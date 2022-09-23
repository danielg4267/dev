package client;
//192.168.0.9
import java.net.*;
import java.util.Scanner;
import java.io.*;

public class ChatApplication {
	
	ServerSocket server;
	int port;
	
	public ChatApplication() {

	}
	
	public static void main(String[] args) throws IOException {
       
		//Client c = new Client();
		//c.joinChat();
		

		
		Socket socket = new Socket("192.168.0.9", 6666);
		System.out.println("Connected");
		Scanner s = new Scanner(System.in);

			int num = s.nextInt();
			String msg = "" + num;
	        socket.getOutputStream().write(msg.getBytes());
	        
	        String rtrn = new String(socket.getInputStream().readAllBytes() , "US-ASCII");
	        System.out.println(rtrn);
			
		
		 
	}
	
	

}
