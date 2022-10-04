package skiplist;

public class Main {

	public static void main(String[] args) {
		SkipList s = new SkipList();
		Node n1 = new Sentinel(null, true);
		Node n2 = new Sentinel(null, false);
		n1.setNext(n2);
		s.insert(4);
		s.insert(2);
		s.insert(3);
		s.print();
		s.delete(4);
		s.print();

	}

}
