package gui;

import java.awt.BorderLayout;

import javax.swing.JFrame;

public class GUI {
	
	private JFrame frame;
	
	public GUI() {
		
		//TODO: GUI should have 
		
		frame = new JFrame("Chatroom");
		frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		frame.setSize(900, 900);
		frame.setLayout(new BorderLayout());
		
	}

}
