package client;
import java.io.*;
import java.net.*;
import java.util.Scanner;

public class Client {
	
	Socket chatroom;
	
	public Client() {
		
	}
	
	public void connect(String IP, int port) {
		try {
			chatroom = new Socket(IP, port);
		}
		catch(IOException IO) {
			System.out.println("Unable to connect.");
		}
	}
	
	public void write(String msg) throws IOException {
		if(chatroom == null) {
			throw new IOException();
		}
		chatroom.getOutputStream().write(msg.getBytes());
	}
	
	public String read() throws IOException{
		if(chatroom == null) {
			throw new IOException();
		}
		return new String(chatroom.getInputStream().readAllBytes(), "US-ASCII");
	}
	
	public void joinChat() {

		Scanner s = new Scanner(System.in);
		String msg = s.next();
		connect("192.168.0.9", 6666);
		try {
			write(msg);
			}
		catch(Exception e) {
			System.out.println("Ya broke it");
		}
		s.close();
		
	}

}
