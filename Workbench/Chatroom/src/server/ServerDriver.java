package server;

public class ServerDriver {
	
	/*
	 * This is not an actual class or main() function I intend to have,
	 * this is for testing purposes only. For now, this is just to start
	 * the server version of the program
	 */
	public static void main(String[] args) {
	
		ChatServer s = new ChatServer("guest");
		
		//change this if the 5555 port doesn't work on your computer - i literally chose a random one that wasn't taken on my computer
		//s.start(1234) 
		s.start(ChatServer.DEFAULT_PORT);
		
	}
}