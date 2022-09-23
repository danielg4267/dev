package server;

public class Driver {
	
	public static void main(String[] args) {
		ChatServer c = new ChatServer();
		c.start(6666);
	}

}
