package client;

import java.io.*;
import java.net.*;
import java.util.Scanner;


/**
 * Client is the client-side
 * version of the program. It is for the
 * user looking to connect to a server.
 * It creates two threads, one each for sending 
 * and receiving messages from the server.
 * It waits for input, and /quit will terminate the 
 * program.
 * 
 * CS5004
 * Summer 2021
 * Independent Project
 * @author Daniel Gonzalez
 *
 */

public class Client {
	
	/**
	 * Socket used to connect with the server.
	 */
	Socket socket;
	
	/**
	 * Thread that will await input from the server, and print it to the user.
	 */
	Receiver readThread;
	
	/**
	 * Thread that awaits input from the user, and sends it to the server.
	 */
	Sender sendThread;
	
	/**
	 * Display used to print messages to the user.
	 */
	PrintStream display;
	
	/**
	 * Input stream to take input from the user.
	 */
	InputStream input;
	
	/**
	 * Scanner to iterate over the input stream.
	 */
	Scanner s;
	
	
	/**
	 * Constructor takes arguments to connect it with an input
	 * and output to take in information and display it to the user.
	 * @param in - input stream to read from the user
	 * @param out - printstream used to display messages from server
	 */
	public Client(InputStream in, PrintStream out) {
		//This is basically the view
		display = out; 
		input = in;
		s = new Scanner(input);
		
		//initialize to null
		socket = null;
		readThread = null;
		sendThread = null;
	}
	
	

	/**
	 * Connects the client to the specified IP and port, if possible.
	 * @param ip - IP address to connect to (should be IPv4)
	 * @param port - port to connect to on that IP
	 */
	public void connect(String ip, int port) {
		if(socket == null) { //not connected
			try {
				display.println("Connecting to server...");
				socket = new Socket(ip, port);
				
				//initiate login sequence with server
				socket.getOutputStream().write(login().getBytes());
				
				//connected and logged in, run threads
				readThread = new Receiver();
				sendThread = new Sender();
				readThread.start();
				sendThread.start();
			}
			catch(IOException e) {
				display.println("Unable to connect, try again.");
			}
		}
		else {
			display.println("Already connected to a server.");
		}
	}
	
	/**
	 * Alerts the server that the user is quitting.
	 */
	public void terminateConnection(){
		
		//short circuit, not even connected yet
		if(socket == null)
			return;
		
		//try to alert the server
		if(!socket.isClosed()) {
			try {
				socket.getOutputStream().write("/quit\n".getBytes());
			}
			catch(IOException e){
				display.println("Unable to send quit signal. Aborting connection.");
			}
			//try to close socket - might already be closed, since there are two threads
			try {
				socket.close();
			}
			catch(IOException e) {
			}
			finally {
				display.println("Disconnected.");
			}
		}

	}
	
	/**
	 * Gets input from the user and formats it for a login
	 * sequence with the server.
	 * @return login command with info from user
	 */
	public String login() {
		
		//server expects "/login [username] [password]"
		String login = "/login ";
		display.println("Enter username:");
		login += s.nextLine().replaceAll(" ", "_") + " ";
		display.println("Enter password:");
		login += s.nextLine().replaceAll(" ", "") + '\n';
		return login;
	}
	
	/**
	 * This class awaits input from the user and sends
	 * it to the server. It only stops when the user types /quit
	 *
	 */
	private class Sender extends Thread{
		
		/**
		 * Output stream from the server socket, used
		 * to send Strings to the server.
		 */
		OutputStream out;

		
		/**
		 * Constructor, sets up the output stream
		 * that this class will use consistently.
		 */
		public Sender() {
			try {
			out = socket.getOutputStream();
			}
			catch(IOException e) {
				display.println("Error getting output stream. Closing connection.");
				terminateConnection();
			}
		}
		
		/**
		 * Main thread run, loops until broken.
		 */
		public void run() {
			
			String msg;
			//get input and send as long as the socket isn't closed and  message isn't /quit
			while(!socket.isClosed() && !(msg = s.nextLine()).equals("/quit")) {
				send(msg);	
			}	
			//finish
			terminateConnection();
			s.close();

		}
		
		/**
		 * Formats a message to send to the server,
		 * then sends it.
		 * @param msg - message to be sent to the server
		 */
		public void send(String msg) {
			//make sure the message ends in a way that the server recognizes
			if(!msg.endsWith("\n"))
				msg += "\n";
			
			try {
				out.write(msg.getBytes());
			}
			catch(IOException e) {
				display.println("Unable to send last message.");
			}
			
		}
		
	}
	
	/**
	 * Thread that receives info from the server
	 * and outputs it to the user. Stops when the server
	 * sends a /quit signal.
	 *
	 */
	private class Receiver extends Thread{
		
		/**
		 * Constructor, takes no arguments, really just useful to
		 * create this object and run it when needed.
		 */
		public Receiver() {}
		
		/**
		 * Main thread run, loops until
		 * "/quit" from the server.
		 */
		public void run() {
			try {
				//holds input from the server
				BufferedReader b = new BufferedReader(new InputStreamReader(socket.getInputStream()));
				String line;
				//read next line
				while ((line = b.readLine()) != null) {
					if(line.equals("/quit")) {
						break; //server booted them, or quit sequence initiated by sender
					}
					display.println(line);
				}
				//end
				terminateConnection();
			}
			//could not get more info/inputstream
			catch(IOException e) {
				display.println("Forcibly disconnected by the host.");
				terminateConnection();
			}

		}
	}
	

}