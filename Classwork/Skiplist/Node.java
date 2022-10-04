package skiplist;

public interface Node {
	
	public void insert(int data);
	
	public boolean isBigger(int data);
	
	public Node findPrevStack();
	
	public Node findNextStack();
	
	public void setNext(Node next);
	
	public void setPrev(Node prev);
	
	public void print();
	
	public Node find(int data);
	
	public int getData();
	
	public Node getNext();
	
	public Node getPrev();
	
	public void delete();
	
	public void setBelow(Node below);
	
	public void setAbove(Node above);
	

}
