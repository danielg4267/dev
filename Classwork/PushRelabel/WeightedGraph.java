package network;

import java.util.LinkedList;

//Adapted from https://algorithms.tutorialhorizon.com/weighted-graph-implementation-java/

public class WeightedGraph {

	 static class Edge {
		 int source;
		 int destination;
		 int flow;
		 int capacity;
		
		 public Edge(int source, int destination, int flow, int capacity) {
			 this.source = source;
			 this.destination = destination;
			 this.flow = flow;
			 this.capacity = capacity;
		 }
	 }
	 
	 static class Node{
		 int e; //u.e from the book, represents flow entering
		 int h; //u.h from the book, represents node height
		 LinkedList<Edge> Adj; //actual adjacency list
		 LinkedList<Integer> pred; //predecessor list, makes it really easy to find nonexistent edges in residual network
		 
		 public Node(int e, int h) {
			 this.e = e;
			 this.h = h;
			 this.Adj = new LinkedList<Edge>();
			 this.pred = new LinkedList<Integer>();
		 }
		 
	 }

	 static class Graph {
		 int vertices;
		 Node[] V;
		
	 Graph(int vertices) {
		 this.vertices = vertices;
		 V = new Node[vertices];
		 for (int i = 0; i <vertices ; i++) {
			 V[i] = new Node(0, 0);
		 }
		 
	 }
	//this was given to me, but i added a "predecessor" set and it keeps track every time an edge is added
	 //it makes it easier to manage the residual network's backwards/non-existent edges
	 public void addEdge(int source, int destination, int capacity) {
		 Edge edge = new Edge(source, destination, 0, capacity);
		 V[source].Adj.addFirst(edge); //for directed graph
		 V[destination].pred.addFirst(source);
	 }
	
	 //pretty simple, just iterates through and prints their connections
	 //i added more details for flow/capacity and excess
	 public void printGraph(){
		 for (int i = 0; i <vertices ; i++) {
			 LinkedList<Edge> list = V[i].Adj;
			 System.out.println("Vertex " + i + ": Height: " + V[i].h +  " Excess: " + V[i].e + " Connected to:");
		 for (int j = 0; j <list.size() ; j++) {
			 System.out.println(list.get(j).destination + " with flow " + list.get(j).flow + " with capacity " + list.get(j).capacity);
			 }
		 }
	 }
	 
	 /************ Begin Code fully implemented by me **************/
	 
	 public void initializePreflow(){
		 //set all node values to 0
		 for (int i=0; i < vertices; i++) {
			 Node v = V[i];
			 v.h = 0;
			 v.e = 0;
			 for(int j = 0; j<v.Adj.size(); j++) {
				 v.Adj.get(j).flow = 0;
			 }
		 }
		 Node s = V[0];
		 s.h = vertices; //initialize height of source node
		 for(int i =0; i < s.Adj.size(); i++) {
			 s.Adj.get(i).flow = s.Adj.get(i).capacity;
			 V[s.Adj.get(i).destination].e = s.Adj.get(i).capacity;
			 s.e -= s.Adj.get(i).capacity;
		 }
	 }
	 
	 public int residualC(int u, int v) {
		boolean uv = false;
		boolean vu = false;
		int edge = isConnected(u, v);
		if(edge > -1) {
			uv = true;
		}
		else {
			edge = isConnected(v, u);
			if(edge > -1) {
				vu = true;
			}
		}
		
		if(uv) {
			//if (u,v) is in E, residual capacity = c(u,v) - f(u, v)
			return V[u].Adj.get(edge).capacity - V[u].Adj.get(edge).flow;
		}
		else if (vu) {
			//if (v,u) is in E, residual capacity = f(v, u)
			return V[v].Adj.get(edge).flow;
		}
		else {
			//they are not connected in any direction in the real graph
			return 0;
		}
		 
	 }
	 
	 public int isConnected(int u, int v) {
		 for(int i = 0; i < V[u].Adj.size(); i++) {
			 if(V[u].Adj.get(i).destination == v) {
				 return i;
			 }
		 }
		 return -1;
	 }
	 public boolean isDownhill(int u) {
		 //check paths in the residual network, and see if u is above v
		 for(int i =0; i< V[u].Adj.size(); i++) {
			 int v = V[u].Adj.get(i).destination;
			 if(V[u].h > V[v].h && residualC(u,v) > 0){
				 return false;
			 }
		 }
		 //backwards edges
		 for(int i =0; i < V[u].pred.size(); i++) {
			 int v = V[u].pred.get(i);
			 if(residualC(u, v) > 0 && V[u].h > V[v].h) {
				 return false;
			 }
		 }
		 return true;
	 }
		 
	public void Push(int u, int v) {
		//this implementation comes straight from the textbook
		int deltaFlow = Math.min(V[u].e, residualC(u, v));
		int edge = isConnected(u, v);
		if(edge > -1){
			V[u].Adj.get(edge).flow = V[u].Adj.get(edge).flow + deltaFlow;
		}
		else {
			edge = isConnected(v,u);
			//simply going to assume that this edge exists, as this method shouldn't be called otherwise
			V[v].Adj.get(edge).flow = V[v].Adj.get(edge).flow - deltaFlow;
		}
		V[u].e -= deltaFlow;
		V[v].e += deltaFlow;
		
	 }
	
	public void Relabel(int u) {
		//make sure it's connected first to avoid null exception
		if(V[u].Adj.size() > 0) {
			
			//find min height amongst all residual edges
			int min = vertices * vertices * vertices; //just some absurd number it could never reach
			for(int i = 0; i<V[u].Adj.size(); i++) {
				int v = V[u].Adj.get(i).destination;
				if(V[v].h < min && residualC(u,v) > 0) {
					min = V[v].h;
				}
			}
			//check edges backwards as well
			for(int i = 0; i<V[u].pred.size(); i++) {
				int v = V[u].pred.get(i);
				if(V[v].h < min && residualC(u,v) > 0) {
					min = V[v].h;
				}
			}
			V[u].h = 1 + min;
		}
	}
	
	public void genericPushRelabel(){
		
		initializePreflow();
		int u = -1;
		//while a node is overflowing, a push or relabel can be done
		while((u=overflow()) > -1) {
			
			//first check for push in its outgoing list
			for(int i = 0; i < V[u].Adj.size(); i++) {
				int v = V[u].Adj.get(i).destination;
				//always double check the node is overflowing, as this loops even after a push
				if(residualC(u, v) > 0 && V[u].h == V[v].h+1 && V[u].e > 0) {
					Push(u, v);
				}
			}
			//check predecessor list, which would only have edges in the residual network
			for(int i = 0; i < V[u].pred.size(); i++) {
				int v = V[u].pred.get(i);
				if(residualC(u, v) > 0 && V[u].h == V[v].h +1 && V[u].e > 0) {
					Push(u, v);
				}
			}
			//check it is downhill for all residual edges connected to it (otherwise it should be pushed) and that it is still overflowing
			if(isDownhill(u) && V[u].e > 0) {
				Relabel(u);
			}
			
		}
	}
	
	public int overflow() {
		for(int i = 0; i < vertices-1; i++) {
			if(V[i].e > 0) {
				return i;
			}
		}
		return -1;
	}
 }
 public static void main(String[] args) {
	 int vertices = 6;
	 Graph graph = new Graph(vertices);
	 graph.addEdge(0, 1, 16);
	 graph.addEdge(0, 2, 13);
	 graph.addEdge(2, 1, 4);
	 graph.addEdge(1, 3, 12);
	 graph.addEdge(3, 2, 9);
	 graph.addEdge(2, 4, 14);
	 graph.addEdge(4, 3, 7);
	 graph.addEdge(3, 5, 20);
	 graph.addEdge(4, 5, 4);
	 graph.printGraph();
	 System.out.println();
	 graph.genericPushRelabel();
	 graph.printGraph();
	 }
}
