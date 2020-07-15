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
    	
    	BTreeNode currNode = this.root;
    	if(currNode == null) {
    		return false;
    	}
    	
    	LinkedList<BTreeNode> stack = new LinkedList<BTreeNode>();
    	
    	while(!currNode.leaf) {
    		stack.push(currNode);
    		for(int child = 0; child < currNode.keys.length; child++) {
    			if(studentId < currNode.keys[child]) {
    				currNode = currNode.children[child];
    				break;
    			}
    			else if(studentId == currNode.keys[child] || child + 1 == currNode.keys.length) {
    				currNode = currNode.children[child + 1];
    				break;
    			}
    		}
    	}
    	
    	boolean found = false;
 
    	for(int value = 0; value < currNode.values.length; value++) {
    		if(studentId == currNode.values[value]) {
    			found = true;
    			if(currNode == this.root) {
    				// delete key and value 
    			}
    			if(currNode.keys.length - 1 > Math.ceil(this.t / 2.0)) {
    				// delete key and value
    				BTreeNode parent = stack.peek();
    				for(int i = 0; i < parent.keys.length; i++) {
    					if(studentId == parent.keys[i]) {
    						parent.keys[i] = currNode.keys[0];
    					}
    				}
    			} else {
    				// delete key and value
    				BTreeNode parent = stack.peek();
    				for(int i = 0; i < parent.keys.length; i++) {
    					// underflow. check conditions and merge
    				}
    			}
    		}
    	}
    	
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
