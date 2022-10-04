package skiplist;

public class Sentinel implements Node{
	
	private Node adjacent;
	private Sentinel above; //should always be in a stack of sentinels
	private Sentinel below;
	private boolean isHead;
	
	public Sentinel(Node other, Sentinel below, boolean isHead) {
		this.adjacent = other;
		this.below = below;
		this.isHead = isHead;
		this.above = null;
	}
	
	public Sentinel(Sentinel below, boolean isHead) {
		this.adjacent = null;
		this.below = below;
		above = null;
		this.isHead = isHead;
	}
	
	public  Sentinel(boolean isHead) {
		this.isHead = isHead;
		this.adjacent = null;
		this.above = null;
		this.below = null;
	}
	
	public void delete() {
		//don't delete the sentinels...
	}
	
	public int getData() {
		if(isHead) {
			return -100000;
		}
		else {
			return 100000;
		}
	}
	
	public void insert(int data) {
		
		if(!isHead) {
			throw new IllegalStateException();
		}

		if(this.adjacent.isBigger(data)) {
			//BOTTOMED OUT, THIS IS THE FINAL LIST
			if(below == null) {
				this.adjacent = new NodeData(this, this.adjacent, data);
				this.adjacent.getNext().setPrev(this.adjacent);
			}
			//THERE'S MORE, ITERATE DOWN
			else {
				below.insert(data);
			}
		}
		//NEXT ONE MIGHT BE ABLE TO INSERT
		else {
			this.adjacent.insert(data);
		}
	}
	
	public Node find(int data) {
		if(!isHead) {
			return null;
		}
		else {
			if(this.adjacent.isBigger(data)) {
				if(below == null) {
					return null;
				}
				else {
					return this.below.find(data);
				}
			}
			else {
				return this.adjacent.find(data);
			}
		}
	}
	
	public Node findPrevStack() {
		if(isHead) {
			if(above != null) {
				return above;
			}
			else {
				above = new Sentinel(this, isHead);
				return above;
			}
		}
		else {
			//not sure how/why you would reach this block, but figured this is what it should do
			return this.adjacent.findPrevStack();
		}
	}

	@Override
	public boolean isBigger(int data) {
		//head should always be smaller, tail always bigger
		return !isHead;
	}

	@Override
	public Node findNextStack() {
		if(!isHead) {
			if(above != null) {
				return above;
			}
			else {
				above = new Sentinel(this, isHead);
				return above;
			}
		}
		else {
			return this.adjacent.findNextStack();
		}
	}

	@Override
	public void setNext(Node next) {
		this.adjacent = next;
		
		
	}
	@Override
	public void setPrev(Node prev) {
		this.adjacent = prev;
		
	}
	
	public Node getNext() {
		return this.adjacent;
	}
	public Node getPrev() {
		return this.adjacent;
	}
	
	public Sentinel findTop() {
		
		
		if(this.above == null) {
			if(this.adjacent instanceof Sentinel) {
				if(below == null) {
					return this;
				}
				else {
					return below.findTop();
				}
			}
			else {
				return this;
			}
		}
		else {
			if(above.getNext() instanceof Sentinel) {
				if(this.adjacent instanceof Sentinel) {
					if(below == null) {
						return this;
					}
					else {
						return below.findTop();
					}
				}
				else {
					return this;
				}
			}
			else {
				return above.findTop();
			}
		}
	}
	
	public void setBelow(Node below) {
		this.below = (Sentinel) below;
	}
	
	public void setAbove(Node above) {
		this.above = (Sentinel) above;
	}
	
	public void print() {
		if(isHead) {
			System.out.print("Head ->");
			this.adjacent.print();
			if(below != null) {
				System.out.println("v");
			}
		}
		else {
			System.out.print("Tail" + '\n');
		}
	}
	
	public Sentinel down() {
		return below;
	}

}
