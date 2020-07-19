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
         * Return recordID for the given StudentID.
         * Otherwise, print out a message that the given studentId has not been found in the table and return -1.
         */

    	BTreeNode cur = this.root;
    	// Check to ensure tree isn't empty
    	if(cur == null) {
    		System.out.println("The given studentId " + studentId + " was not found in the table.");
    		return -1;
    	}

    	// search for correct leaf node
    	while(cur != null && !cur.leaf) {
    		for(int child = 0; child < cur.n; child++) {
    			// Check for left-of-value (LT) traverse
    			if(studentId < cur.keys[child]) {
    				cur = cur.children[child];
    				break;
    			}
    			// Check for rightmost link traverse
    			else if(studentId == cur.keys[child] || child + 1 == cur.n) {
    				cur = cur.children[child + 1];
    				break;
    			}
    		}
    	}
    	
    	// Check for key in leaf node
    	if(cur != null) {
        	for (int i = 0; i < cur.n; i++)
        	{
        		if (studentId == cur.keys[i])
        		{
        			// Key found
        			return cur.values[i];
        		}
        	}
    	}
    	
    	// Value was not found in the leaf node
    	System.out.println("The given studentId " + studentId + " was not found in the table.");
        return -1;
    }

    BTree insert(Student student) {
        /**
         * Insert into the B+Tree.
         * Also, insert in student.csv after inserting in B+Tree.
         */

    	long key;
    	if(student == null) {
    		return null;
    	}
    	else {
    		key = student.studentId;
    	}
    	if(this.root == null) {
    		this.root = new BTreeNode(this.t, true);
    		this.root.keys[0] = key;
    		this.root.values[0] = key;
    	}
    	else {
    		if(this.root.n == (2 * t) - 1) {
    			BTreeNode newRoot = new BTreeNode(this.t, false);
    			newRoot.children[0] = this.root;
    			split(newRoot, 0);
    			
    			int index = 0;
    			if(newRoot.keys[0] < key) {
    				index++;
    			}
    			insertIntoNode(newRoot.children[index], key);
    			this.root = newRoot;
    			
    		}
    		else {
    			insertIntoNode(this.root, key);
    		}
    	}

		insertToFile("Student.csv", student);
        return this;
    }
    
	public void insertIntoNode(BTreeNode node, long key) {
		if(node == null) {
			node = new BTreeNode(this.t, true);
		}
		int index = node.n - 1;
		
		if(node.leaf) {
			while(index >= 0 && node.keys[index] > key) {
				node.keys[index + 1] = node.keys[index];
				node.values[index + 1] = node.values[index];
				index--;
			}
			node.keys[index + 1] = key;
			node.values[index + 1] = key;
			node.n++;
		} else {
			while(index >= 0 && node.keys[index] > key) {
				index--;
			}
			if(node.children[index + 1] != null && node.children[index + 1].n == (2 * this.t) - 1) {
				split(node, index + 1);
				if(node.keys[index + 1] < key) {
					index++;
				}
			}
			insertIntoNode(node.children[index + 1], key);
		}

	}
	
	private void split(BTreeNode node, int index) {
		BTreeNode child = node.children[index];
		BTreeNode temp = new BTreeNode(child.t, child.leaf);
		temp.n = this.t - 1;
		
		for(int offset = 0; offset < this.t - 1; offset++) {
			temp.keys[offset] = child.keys[offset + this.t];
			if(child.leaf) {
				temp.values[offset] = child.values[offset + this.t];
			} else {
				temp.children[offset] = child.children[offset + this.t];
			}
		}
		child.n = this.t - 1;
		
		for(int offset = 0; offset >= index + 1; offset--) {
			node.children[offset + 1] = node.children[offset];
		}
		
		node.children[index + 1] = temp;
		
		for(int offset = node.n - 1; offset >= index; offset--) {
			node.keys[offset + 1] = node.keys[offset];
			if(node.leaf) {
				node.values[offset + 1] = node.values[offset];
			}
		}
		
		node.keys[index] = child.keys[this.t - 1];
		if(node.leaf) {
			node.values[index] = child.values[this.t - 1];
		}
		node.n++;
	}
	
	public void insertToFile(String csv, Student s) {
		BufferedWriter bw = null;

		try {
			bw = new BufferedWriter(new FileWriter(csv, true));
			
			String entry = s.studentId+","+s.studentName+","+s.major+","+s.level+","+s.age+","+s.recordId+"\n";

			bw.append(entry);
			bw.close();
		} catch(FileNotFoundException e) {
			e.printStackTrace();
		} catch(IOException e) {
			e.printStackTrace();
		} finally {
			if(bw != null) {
				try {
					bw.close();
				} catch(IOException e) {
					e.printStackTrace();
				}
			}
		}
	}
    
    boolean delete(long studentId) {
        /** 
         * Delete studentId from the B+Tree.
         * Also, delete in student.csv after deleting in B+Tree, if it exists.
         * Return true if the student is deleted successfully otherwise, return false.
         */
    	
    	BTreeNode node = this.root;
    	
    	// "delete" from empty tree
    	if(node == null) {
    		return false;
    	}
    	
    	LinkedList<BTreeNode> parent_stack = new LinkedList<BTreeNode>();
    	LinkedList<Integer> index_stack = new LinkedList<Integer>();

    	// search for leaf node and track path
    	while(!node.leaf) {
    		for(int child = 0; child < node.n; child++) {
    			// left node
    			if(studentId < node.keys[child]) {
    				node = node.children[child];
    	    		parent_stack.push(node);
    				index_stack.push(child);
    				break;
    			}
    			// right node
    			else if(studentId == node.keys[child] || child + 1 == node.n) {
    				node = node.children[child + 1];
    	    		parent_stack.push(node);
    				index_stack.push(child);
    				break;
    			}
    		}
    	}
    	
    	boolean found = false;
 
    	// determine if sid in leaf node
    	for(int index = 0; index < node.n; index++) {
    		if(studentId == node.values[index]) {
    			found = true;
    			break;
    		}
    	}
    	
    	// update nodes along path
    	if(found) {
    		while(!parent_stack.isEmpty()) {
    			BTreeNode parent = parent_stack.pop();
    			int index = index_stack.pop();
    			deleteFromNode(parent, index);
    			// fill children
    			if(parent.children[index] != null && parent.children[index].n < this.t) {
    				fill(parent, index);
    			}
    		}
    		// delete removed student from the csv file
    		deleteFromFile("Student.csv", studentId);
    	}
    	return found;
    }
    
    public void deleteFromNode(BTreeNode node, int index) {
    	/**
    	 * method to remove a key or key-value pair from a node
    	 */
    	
    	// leaf node
    	if(node.leaf) {
    		for(int i = index + 1; i < node.n; i++) {
    			node.keys[i - 1] = node.keys[i];
    			node.values[i - 1] = node.values[i];
    		}
    		node.n--;
    	}
    	// internal node
    	else {
    		// borrow from predecessor
    		if(node.children[index].n >= node.t) {
    			BTreeNode child = node.children[index];
    			BTreeNode predecessor = getPred(child);
    			node.keys[index] = predecessor.keys[0];
    			deleteFromNode(predecessor, 0);
    		// borrow from successor
    		} else if(node.children[index + 1].n >= t) {
    			BTreeNode child = node.children[index + 1];
    			BTreeNode successor = getSucc(child);
    			node.keys[index] = successor.keys[successor.n - 1];
    			deleteFromNode(successor, successor.n);
    		// merge if neither predecessor nor successor have sufficient children
    		} else {
    			merge(node, index);
    			deleteFromNode(node, index);
    		}
    	}
    }

    public BTreeNode getSucc(BTreeNode node) {
    	/**
    	 * return successor of a given node
    	 */
    	BTreeNode curr = node;
    	while(!curr.leaf) {
    		curr = curr.children[0];
    	}
    	return curr;
    }

    public BTreeNode getPred(BTreeNode node) {
    	/**
    	 * return predecessor of a given node
    	 */
    	BTreeNode curr = node;
    	while(!curr.leaf) {
    		curr = curr.children[curr.n];
    	}
    	return curr;
    }
    
    public void merge(BTreeNode node, int index) {
    	/**
    	 * merge two of a node's children (child and sibling)
    	 */
    	BTreeNode child = node.children[index];
    	BTreeNode sib = node.children[index + 1];
    	
    	// update middle key/value of child to reference parent at given index
    	child.keys[node.t - 1] = node.keys[index];
    	if(node.leaf) {
        	child.values[node.t - 1] = node.values[index];
    	}
    	
    	// update child to reference sibling key/value/child sets after t
    	for(int i = 0; i < sib.n; i++) {
    		child.keys[node.t + i] = sib.keys[i];
    		if(child.leaf) {
    			child.values[node.t + i] = sib.values[i];
    		} else {
    			child.children[node.t + i] = sib.children[i];
    		}		
    	}
    	
    	// update parent to reference previous key/value/children sets
    	for(int i = index + 1; i < node.n; i++) {
    		node.keys[i - 1] = node.keys[i];
    		if(child.leaf) {
        		node.values[i - 1] = node.values[i];
    		} else {
    			node.children[i - 1] = node.children[i];
    		}
    	}
    	
    	// sibling now merged into child, as well as element of parent node at index
    	child.n += sib.n + 1;
    	node.n--;
	}
	
    
    public void fill(BTreeNode node, int index) {
    	if(index != 0 && node.children[index - 1].n >= t) {
    		borrowFromPred(node, index);
    	} else if(index != node.n && node.children[index + 1].n >= t) {
    		borrowFromSucc(node, index);
    	} else {
    		if(index != node.n) {
    			merge(node, index);
    		} else {
    			merge(node, index - 1);
    		}
    	}
    }
    
    public void borrowFromPred(BTreeNode node, int index) {
    	/**
    	 * Update node to reference node to the left (predecessor)
    	 */
    	BTreeNode child = node.children[index];
    	BTreeNode sib = node.children[index - 1];
    	
    	// update keys, values, and children to reference next in order
    	// creating space for new child
    	for(int i = child.n - 1; i >= 0; i--) {
    		child.keys[i + 1] = child.keys[i];
    		if(child.leaf) {
    			child.values[i + 1] = child.values[i];
    		} else {
    			child.children[i + 1] = child.children[i];
    		}
    	}
    	
    	// add new child and reference key/value when appropriate
    	child.keys[0] = node.keys[index - 1];
    	if(child.leaf) {
    		child.values[0] = node.values[index - 1];
    	} else {
    		child.children[0] = sib.children[sib.n];
    	}
    	
    	// add to the degree of the child and remove from the sibling
    	child.n += 1;
    	sib.n -= 1;
    }
    
    public void borrowFromSucc(BTreeNode node, int index) {
    	/**
    	 * Update node to reference node to the right (successor)
    	 */
    	BTreeNode child = node.children[index];
    	BTreeNode sib = node.children[index + 1];
    	
    	// add child and key/value reference at index when appropriate
    	child.keys[child.n] = node.keys[index];
    	if(child.leaf) {
    		child.values[child.n] = node.keys[index];
    	} else {
    		child.children[child.n + 1] = sib.children[0];
    	}
    	
    	// update reference to first element in sibling
    	node.keys[index] = sib.keys[0];
    	
    	// update keys and values/children to previous, creating space for new
    	// child
    	for(int i = 1; i < sib.n; i++) {
    		sib.keys[i - 1] = sib.keys[i];
    		if(sib.leaf) {
    			sib.values[i - 1] = sib.values[i];
    		} else {
    			sib.children[i - 1] = sib.children[i];
    		}
    	}
    	
    	// add to the degree of the child and remove from the sibling
    	child.n += 1;
    	sib.n -= 1;
    }
    
    public void deleteFromFile(String csv, long key) {
    	/**
    	 * Search csv file for instances of deleted key and remove line by
    	 * writing to a temporary file
    	 */
		File input = new File(csv);
		File temp = new File("temp.csv");
		BufferedReader br = null;
		BufferedWriter bw = null;
		String line = "";
		String dilimiter = ",";
		try {
			br = new BufferedReader(new FileReader(input));
			bw = new BufferedWriter(new FileWriter(temp));
			while((line = br.readLine()) != null) {
				// get student ID from csv and check if it matches key
				long sid = Long.parseLong(line.split(dilimiter)[0]);
				if(key == sid) {
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
	
    List<Long> print() {
        /**
         * Return a list of recordIDs from left to right of leaf nodes.
         */

        List<Long> listOfRecordID = new ArrayList<>();

        // Start at the leftmost leaf node
        BTreeNode cur = getSucc(root);
        do
        {
        	// Print each valid value in the node
        	for (long i : cur.values)
        	{
        		if (i == 0) continue;
        		listOfRecordID.add(i);
        	}
        	// Move on to next node
        	cur = cur.next;        	
        }
        // End at rightmost node
        while (cur.next != null);
        
		return listOfRecordID;
	}
}
