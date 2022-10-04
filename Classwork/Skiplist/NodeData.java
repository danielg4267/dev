package skiplist;
import java.util.Random;

public class NodeData implements Node {
	
	private Node next;
	private Node prev;
	private Node above;
	private Node below;
	private int data;
	
	public NodeData(Node prev, Node next, Node below, int data) {
		this.prev = prev;
		this.next = next;
		this.below = below;
		this.data = data;
		createStacks();
	}
	
	public NodeData(Node prev, Node next, int data) {
		this.next = next;
		this.prev = prev;
		this.below = null;
		this.data = data;
		createStacks();
		
	}
	
	//helper function for constructor
	private void createStacks() {
		Random r = new Random();
		if(r.nextInt(2) == 1) {
			Node prev = this.prev.findPrevStack();
			Node next = this.next.findNextStack();
			this.above = new NodeData(prev, next, this, data);
			prev.setNext(this.above);
			next.setPrev(this.above);
			
		}
		else {
			this.above = null;
		}
		
	}
	public Node getNext(){
		return next;
	}
	
	public Node getPrev() {
		return prev;
	}
	
	public void setBelow(Node below) {
		this.below = below;
	}
	
	public void setAbove(Node above) {
		this.above = above;
	}
	
	public void delete() {

		this.prev.setNext(next);
		this.next.setPrev(prev);
		if(this.below != null) {
			this.below.setAbove(null);
			this.below.delete();
		}
		if(this.above != null) {
			this.above.setBelow(null);
			this.above.delete();
		}
	}
	
	public int getData() {
		return data;
	}
	
	public void insert(int data) {
		if(this.data <= data) {
			//NEXT IS TOO LARGE
			if(this.next.isBigger(data)) {
				//BOTTOMED OUT
				if(below == null) {
					this.next = new  NodeData(this, this.next, data);
					this.next.getNext().setPrev(this.next);

				}
				//ITERATE DOWN
				else {
					this.below.insert(data);
				}
			}
			else {
				this.next.insert(data);
			}
		}
	}
	
	public Node find(int data) {
		
		if(this.data == data) {
			return this;
		}
		else if(this.next.isBigger(data)) {
			//bottomed out, and couldn't find it
			if(below == null) {
				return null;
			}
			//iterate down and check next list
			else {
				return this.below.find(data);
			}
		}
		//next might be it
		else {
			return this.next.find(data);
		}
	}
	
	public boolean isBigger(int data) {
		return this.data > data;
	}
	
	public Node findPrevStack() {
		if (this.above != null) {
			return this.above;
		}
		else {
			return prev.findPrevStack();
		}
	}
	
	public Node findNextStack() {
		if(this.above != null) {
			return this.above;
		
		}
		else {
			return this.next.findNextStack();
		}
	}

	@Override
	public void setNext(Node next) {
		this.next = next;
		
	}

	@Override
	public void setPrev(Node prev) {
		this.prev = prev;
		
	}
	
	public void print() {
		
		System.out.print(data + "->");
		this.next.print();
		
	}

}
