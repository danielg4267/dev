package server;

import java.io.*;
import java.net.*;

public class ChatServer {
	
	private ServerSocket server;
	
	
	public void start(int port) {
		
		try {
			server = new ServerSocket(port);
			while(true) {
				System.out.println("Waiting for connection");
				Socket client = server.accept();
				System.out.println("Accepted connection from: " + client);
				new ClientConnection(client).start();

			}
		}
		catch(IOException IO) {
			IO.printStackTrace();
		}
		
	}
	

}

/*
 public void start(int port) {
		try {
			server = new ServerSocket(port);
			String msg = "";
			while(!msg.equals("exit\n")) {
				System.out.println("Waiting for connection");
				Socket client = server.accept();
				System.out.println("Connected to " + client);
				
				System.out.println(new String(client.getInputStream().readAllBytes()));
				OutputStream out = client.getOutputStream();
				out.write("HElloWorld\n".getBytes());
				client.close();
				System.out.println("Closed client connection.");
			}
		}
		catch(IOException IO) {
			System.out.println("AAAH!");
		}
	}
 */