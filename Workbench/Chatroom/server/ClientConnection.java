package server;

import java.net.*;
import java.io.*;

public class ClientConnection extends Thread{
	
	Socket client = null;
	
	public ClientConnection(Socket client) {
		
		this.client = client;
		
	}
	

	@Override
	public void run() {
		try {
			//BufferedReader in = new BufferedReader(new InputStreamReader(client.getInputStream()));
			InputStream in = client.getInputStream();
			OutputStream out = client.getOutputStream();
			System.out.println("run() has been called!");
			String msg = new String(in.readAllBytes(), "US-ASCII");

			
			System.out.println("We're running!");
			while(msg != "exit") {
				System.out.println("Client typed: " + msg);
				out.write(("You typed: " + msg).getBytes());
				
				msg = new String(in.readAllBytes(), "US-ASCII");
				
				
			}
			System.out.println("Not running now!");
		}
		catch(IOException e) {
			e.printStackTrace();
		}
		
	}

}
