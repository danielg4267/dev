package client;

import java.net.InetAddress;
import java.net.UnknownHostException;
import java.util.Scanner;

import server.ChatServer;


public class ClientDriver {
	
	/*
	 * This is not an example of a class or an actual main() function that I plan to have,
	 * especially because it only connects to a server on your computer by default.
	 * This is for testing and demonstration purposes only.
	 * 
	 * Running multiple instances of this driver will simulate multiple users connecting
	 */
	public static void main(String[] args) {
		String ip;
		try {
			//just default to get your IP
			ip = InetAddress.getLocalHost().getHostAddress();
		}
		catch(UnknownHostException e){
			//for some reason, could not get it
			Scanner s = new Scanner(System.in);
			System.out.println("Enter your IPv4 Address:");
			ip = s.nextLine();
		}
		Client c = new Client(System.in, System.out);
		
		//change this line if you'd like to see what happens when you put in incorrect data
		//c.connect("000.00.0.0", 999999999) or something
		c.connect(ip, ChatServer.DEFAULT_PORT);
		
		
	}
}