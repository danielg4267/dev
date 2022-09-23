package server;

import java.net.ServerSocket;
import java.net.Socket;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.OutputStream;

import java.util.Hashtable;
import java.util.Random;

import java.time.LocalTime;
import java.time.ZonedDateTime;
import java.time.temporal.ChronoUnit;

/**
 * Runs the server version of the chatroom.
 * Accepts client connections, creates separate threads for
 * each, and sends/receives messages from every thread.
 * 
 * CS5004
 * Summer 2021
 * Independent Project
 * @author Daniel Gonzalez
 *
 */
public class ChatServer {
	
	public static final int DEFAULT_PORT = 5555;
	
	/**
	 * ServerSocket to accept any incoming connections.
	 */
	private ServerSocket server;
	
	/**
	 * Stores all connections with username/socket pairs
	 */
	private Hashtable<String, Socket> connections;

	/**
	 * Whether this server requires a password to join.
	 */
	private boolean hasPassword;
	
	/**
	 * Password needed to join server
	 */
	private String password;

	
	/**
	 * No argument constructor, initializes values to defaults.
	 * No password, no connections.
	 */
	public ChatServer() {

		password = null;
		hasPassword = false;
		connections = new Hashtable<String, Socket>();
	}
	
	/**
	 * One argument constructor, creates a server instance
	 * with a password if true, nothing if false.
	 * @param hasPassword - boolean, whether to generate a password
	 */
	public ChatServer(boolean hasPassword) {

		this.hasPassword = hasPassword;
		password = generatePassword(); 
		System.out.println("Password is " + password);
		connections = new Hashtable<String, Socket>();
	}
	
	/**
	 * One argument constructor, takes a string, sets it as the server
	 * password.
	 * @param password - server password
	 */
	public ChatServer(String password) {
		
		this.hasPassword = true;
		this.password = password;
		System.out.println("Password is " + password);
		connections = new Hashtable<String, Socket>();
		
	}
	
	/**
	 * Password generator, returns a random String
	 * of 10 characters.
	 * @return random string of 10 characters
	 */
	private String generatePassword() {
		String characters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
                + "0123456789-=~!@#$%^&*()_+"
                + "abcdefghijklmnopqrstuvxyz";
		String password = "";
		Random r = new Random();	
		//Really simple, could definitely be improved
		for(int i = 0; i<10; i++) {
			password += characters.charAt(r.nextInt(characters.length()));
		}
		return password;
	}
	
	/**
	 * Opens the server socket to start receiving connections
	 * on the specified port. Continually accepts connections.
	 * @param port - open port to listen on
	 */
	public void start(int port) {
		try {
			server = new ServerSocket(port);
			
			//continually waits for connections
			while(true) {
				System.out.println("Waiting for connection");
				Socket client = server.accept();
				
				//new thread for this client
				Thread r = new ClientHandler(client);
				r.start();
				System.out.println("Connected to " + client);
			}
		}
		catch(IOException e) {
			e.printStackTrace();
		}
	}
	

	/**
	 * Removes any users from the list that are currently not 
	 * connected. Does not disconnect those that are still connected.
	 */
	public void removeUsers(){
		connections.entrySet().removeIf(sockets->sockets.getValue().isClosed());
	}
	
	
	/**
	 * ClientHandler is a thread that runs for every client
	 * that connects. Each one can store the socket it is stored in,
	 * and stores a username for the client that is connected. 
	 *
	 */
	private class ClientHandler extends Thread{
		
		/**
		 * Client socket that this thread receives from.
		 */
		private Socket client;
		
		/**
		 * Username entered for this user.
		 */
		private String username;
		
		/**
		 * Socket output stream to print alerts to
		 */
		private OutputStream out;
		
		/**
		 * Socket input stream to read from
		 */
		private InputStream in;
		
		/**
		 * Exit variable to stop the thread from running.
		 */
		private boolean exit;
		
		/**
		 * Constructor, takes a client and sets up this thread's
		 * attributes before start() is called.
		 * @param client - socket this thread will read from
		 */
		public ClientHandler(Socket client) {
			this.client = client;
			exit = false;
			username = ""; //to start, user should log in after this
			try {
			out = client.getOutputStream();
			in = client.getInputStream();
			}
			catch(IOException e) {
				System.out.println("Could not find in/out streams. Terminating connection.");
				terminateConnection();
				
			}
		}
		
		public void run() {
			
			try {
				//reads input stream
				BufferedReader b = new BufferedReader(new InputStreamReader(in));
				String line;
			//continually reads the stream for newLine characters, runs when \n is read and the line is not null
				while ( (line = b.readLine()) != null) {
					processMsg(line); //handle the input
					
					//may have been an exit command
					if(exit) 
						break;
				}
			}		
			//Couldn't read stream, user disconnected, abort
			catch(IOException e) {
				terminateConnection();	
				//if logged in, let users know who disconnected
				if(!username.equals("")) 
					sendAlert(username + " left the chat.");

			}
		}
		
		
		/**
		 * Takes in a String and calls the proper method depending
		 * on its contents. Commands should start with '/'
		 * @param msg - message to interpret
		 */
		public void processMsg(String msg) {
			//short circuit, check if it's a command
			if(msg.charAt(0) != '/') {
				sendMsg(msg);
				return;
			}
				
			String[] cmd = msg.split(" ");

			//check command, run proper method based on it
			switch(cmd[0]) {
			
				case "/quit":
					terminateConnection();
					sendAlert(username + " left the chat.");
					break;
					
				case "/login":
					login(cmd);
					break;
					
				case "/online":
					online();
					break;
					
				//unrecognized command
				default:
					sendMsg(msg);
				}		
			}
		
		/**
		 * Checks that the user's input matches what is expected, ie
		 * username isn't empty string, the password matches, and they aren't
		 * already logged in. Adds them to the list of users to begin receiving input
		 * if successful. Disconnects from socket otherwise.
		 * @param login - array of strings containing [login command, username, password]
		 */
		public void login(String[] login) {
			//not logged in yet
			if (username.equals("")){
				try {
					//empty username or wrong password
					if((hasPassword && !login[2].equals(password)) || login[1].equals("")) {
						sendUser("Invalid login.");
						terminateConnection();
					}
					//already a user with this name, or this socket is already used
					else if (connections.containsValue(client) 
							|| connections.containsKey(login[1])){
						sendUser("Duplicate connection.");
						terminateConnection();
					}
					else {
						username = login[1];
						//final check, only add if not actually there - do not override existing connections
						connections.putIfAbsent(username, client);
						System.out.println("Successful login.");
						sendAlert(username + " joined the chat.");
						sendUser("Welcome, " + username + ".");
						
					}
				}
				//Handed it a strange array
				catch(ArrayIndexOutOfBoundsException e) {
					sendUser("Invalid login.");
					terminateConnection();
				}
			}
			else {
				sendUser("Already logged in.");
			}
		}
		
		/**
		 * Sends the client saved to this instance a list of all users connected
		 * to the overall server
		 */
		public void online() {
			String usernames =  "Online:" + '\n';
			for(String user: connections.keySet()) {
				usernames += (user + '\n');
			}
			sendUser(usernames);
		}
		
		/**
		 * Formats and sends a message to all users connected to the server.
		 * Sends with information identifying this client.
		 * @param message - message to send to all users
		 */
		public void sendMsg(String message) {
			//format message for final send
			LocalTime t = ZonedDateTime.now().toLocalTime().truncatedTo(ChronoUnit.SECONDS);
			message ="[" +t +"]" + " " + username + ": " + message;
			sendAll(message);
		}
		
		/**
		 * Formats and sends an alert to all users connected to the server.
		 * Sends as if sent from the server.
		 * @param message - alert to be sent to all users
		 */
		public void sendAlert(String message) {
			LocalTime t = ZonedDateTime.now().toLocalTime().truncatedTo(ChronoUnit.SECONDS);
			message ="[" +t +"] Server: " + message;
			sendAll(message);
			
		}

		/**
		 * Sends only this handler's client a message. 
		 * Formats it and sends it from the server.
		 * @param msg - message to send to user
		 */
		public void sendUser(String msg) {
			if (!msg.endsWith("\n"))
				msg += "\n";
			
			LocalTime t = ZonedDateTime.now().toLocalTime().truncatedTo(ChronoUnit.SECONDS);
			msg = "[" +t +"] Server: " + msg;
			
			try {
				out.write((msg).getBytes());
			}
			catch(IOException e) {
				terminateConnection();
			}
		}
		
		/**
		 * Sends all users a string. Does not format it.
		 * @param message - string to send all users
		 */
		public void sendAll(String message) {
			
			if(!message.endsWith("\n"))
				message += "\n";
			
			String msg = message;
			
			//send message to each socket in the hashtable
			connections.entrySet().forEach((sockets)->{
				try {
					sockets.getValue().getOutputStream().write(msg.getBytes());
				} catch (IOException e) {
					//cannot send message to this user, continue loop and ignore it 
					//can't removeUsers() or disconnect them here, as that would disrupt the hashtable/entryset
					System.out.println("Unable to send message to " + sockets.getKey());
				}
			});
		}
		
		
		/**
		 * Attempts to terminate connection safely with this client and end the run loop,
		 * sends a quit command to the client and closes the socket.
		 */
		public void terminateConnection() {

			try {
			out.write("/quit\n".getBytes()); //quit signal for client reader
			}
			catch(IOException e) {
				System.out.println("Unable to send quit signal. Forcibly closing connection.");
			}
			try {
				client.close();
			}
			catch(IOException e) {
				System.out.println("Connection already closed.");
			}
			finally {
				removeUsers();
				exit = true; //no longer connected, end run loop
				System.out.println(username + " disconnected.");
			}
			
		}
	}
		
}



