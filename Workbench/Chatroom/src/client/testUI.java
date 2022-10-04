package client;

import javax.swing.*;
import java.awt.BorderLayout;
import java.awt.Container;

public class testUI {
	
	public static void main(String[] args) {
		JFrame frame = new JFrame("Chatroom");
		frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		frame.setSize(900, 900);
		
		//Set Layout Manager
		
		//ADd Swing Components to Content Area
		
		//Add behavior
		
		frame.setLayout(new BorderLayout());
		JTextArea txt = new JTextArea();
		Container c = frame.getContentPane();
		JButton b = new JButton("Click Me");
		c.add(txt, BorderLayout.CENTER);
		c.add(b, BorderLayout.SOUTH);
		//frame.add(b);
		frame.setVisible(true);
	}

}
