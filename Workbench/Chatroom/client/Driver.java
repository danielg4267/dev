//package client;
//192.168.0.9
import java.net.*;
import java.util.Scanner;
import java.io.*;

public class Driver {
	
	
	public static void main(String[] args) {
		

		try{
		Socket socket = new Socket("192.168.0.9", 6666);
		System.out.println("Connected");
		Scanner s = new Scanner(System.in);

			int num = s.nextInt();
			String msg = "" + num;
	        socket.getOutputStream().write(msg.getBytes());
	        
	        String rtrn = new String(socket.getInputStream().readAllBytes() , "US-ASCII");
	        System.out.println(rtrn);
	        socket.close();
			
		}
		catch(IOException e){
			System.out.println("It broke!");
		}
		 
	}
	
	

}
