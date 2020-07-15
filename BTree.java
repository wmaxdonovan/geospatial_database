/**
 * Do NOT modify.
 * This is the class with the main function
 */

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.LinkedList;
import java.util.List;

/**
 * B+Tree Structure
 * Key - StudentId
 * Leaf Node should contain [ key,recordId ]
 */
class BTree {

    /**
     * Pointer to the root node.
     */
    private BTreeNode root;
    /**
     * Number of key-value pairs allowed in the tree/the minimum degree of B+Tree
     **/
    private int t;

    BTree(int t) {
        this.root = null;
        this.t = t;
    }

    long search(long studentId) {
        /**
         * TODO:
         * Implement this function to search in the B+Tree.
         * Return recordID for the given StudentID.
         * Otherwise, print out a message that the given studentId has not been found in the table and return -1.
         */
        return -1;
    }

    BTree insert(Student student) {
        /**
         * TODO:
         * Implement this function to insert in the B+Tree.
         * Also, insert in student.csv after inserting in B+Tree.
         */
        return this;
    }

    boolean delete(long studentId) {
        /**
         * TODO:
         * Implement this function to delete in the B+Tree.
         * Also, delete in student.csv after deleting in B+Tree, if it exists.
         * Return true if the student is deleted successfully otherwise, return false.
         */
    	
    	BTreeNode node = this.root;
    	
    	// "delete" from empty tree
    	if(node == null) {
    		return false;
    	}
    	
    	LinkedList<BTreeNode> stack = new LinkedList<BTreeNode>();
    	
    	// search for leaf node
    	while(!node.leaf) {
    		stack.push(node);
    		for(int child = 0; child < node.n; child++) {
    			if(studentId < node.keys[child]) {
    				node = node.children[child];
    				break;
    			}
    			else if(studentId == node.keys[child] || child + 1 == node.keys.length) {
    				node = node.children[child + 1];
    				break;
    			}
    		}
    	}
    	
    	boolean found = false;
 
    	// search node for key-value pair
    	for(int index = 0; index < node.n; index++) {
    		if(studentId == node.values[index]) {
    			found = true;
    			deleteFromNode(node, index);
    		}
    	}
    	
    	// delete line from csv
    	if(found) {
    		File input = new File("Student.csv");
    		File temp = new File("tempStudent.csv");
    		BufferedReader br = null;
    		BufferedWriter bw = null;
    		String line = "";
    		String dilimiter = ",";
    		try {
    			br = new BufferedReader(new FileReader(input));
    			bw = new BufferedWriter(new FileWriter(temp));
    			while((line = br.readLine()) != null) {
    				int sid = Integer.parseInt(line.split(dilimiter)[0]);
    				if(studentId == sid) {
    					continue;
    				}
    				else {
        				bw.write(line + '\n');
    				}
    			}
    		} catch(FileNotFoundException e) {
    			e.printStackTrace();
    		} catch(IOException e) {
    			e.printStackTrace();
    		} finally {
    			if(br != null) {
    				try {
    					br.close();
    					bw.close();
    					temp.renameTo(input);
    				} catch(IOException e) {
    					e.printStackTrace();
    				}
    			}
    		}
    	}
    	
    	return found;
    }
    
    public void deleteFromNode(BTreeNode node, int index) {
    	if(node.leaf) {
    		for(int i = index + 1; i < node.n; i++) {
    			node.keys[i - 1] = node.keys[i];
    			node.values[i - 1] = node.values[i];
    		}
    		node.n--;
    	}
    	else {
    		if(node.children[index].n >= node.t) {
    			long predecessor = getPred(node, index);
    			node.keys[index] = predecessor;
    			delete(predecessor);
    		} else if(node.children[index + 1].n >= t) {
    			long successor = getSucc(node, index);
    			node.keys[index] = successor;
    			delete(successor);
    		} else {
    			merge(node, index);
    			delete(node.keys[index]);
    		}
    	}
    }
    
    public long getSucc(BTreeNode node, int index) {
    	BTreeNode curr = node.children[index];
    	while(!curr.leaf) {
    		curr = curr.children[0];
    	}
    	return curr.keys[0];
    }

    public long getPred(BTreeNode node, int index) {
    	BTreeNode curr = node.children[index];
    	while(!curr.leaf) {
    		curr = curr.children[curr.n];
    	}
    	return curr.keys[curr.n - 1];
    }
    
    public void merge(BTreeNode node, int index) {
    	BTreeNode child = node.children[index];
    	BTreeNode sib = node.children[index + 1];
    	
    	child.keys[node.t - 1] = node.keys[index];
    	child.values[node.t - 1] = node.values[index];
    	
    	for(int i = 0; i < sib.n; i++) {
    		child.keys[node.t + i] = sib.keys[i];
    		if(child.leaf) {
    			child.values[node.t + i] = sib.values[i];
    		} else {
    			child.children[node.t + i] = sib.children[i];
    		}		
    	}
    	
    	for(int i = index + 1; i < node.n; i++) {
    		node.keys[i - 1] = node.keys[i];
    		if(child.leaf) {
        		node.values[i - 1] = node.values[i];
    		} else {
    			node.children[i - 1] = node.children[i];
    		}
    	}
    	child.n += sib.n + 1;
    	node.n--;
    }
    List<Long> print() {

        List<Long> listOfRecordID = new ArrayList<>();

        /**
         * TODO:
         * Implement this function to print the B+Tree.
         * Return a list of recordIDs from left to right of leaf nodes.
         *
         */
        return listOfRecordID;
    }
}
