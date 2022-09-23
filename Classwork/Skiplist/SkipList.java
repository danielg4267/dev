package skiplist;

import java.util.ArrayList;

public class SkipList {
	
	private Sentinel topHead;
	
	public SkipList() {
		this.topHead = new Sentinel(null, true);
		this.topHead.setNext(new Sentinel(null, false));
		this.topHead.getNext().setPrev(topHead);
	}
	
	public void insert(int data) {
		topHead.insert(data);
		topHead = topHead.findTop();
	}
	
	public Node find(int data) {
		
		return topHead.find(data);
	}
	
	public void print() {
		Sentinel n = topHead;
		while(n.down() != null) {
			n.print();
			n = n.down();
		}
		System.out.println("Bottom:");
		n.print();
	}
	
	public void delete(int data) {
		topHead.find(data).delete();
		
	}

}
