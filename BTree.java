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
import java.io.PrintWriter;
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

		BTreeNode node = this.root;

		 if(!node.leaf) {
    		for(int child = 0; child < node.n; child++) {
				insert(student);
				if(student == null){
					return null;
				}
				else {
					if (node.n < node.t) {
						insert(student); //not sure this line is right
						student = null;
						return this; //? 
					}
					else {
						//split
						if (node==this.root) {
							//new node w pointer to inserted ? and update root ptr
							BTreeNode newnode = new BTreeNode(t, false);
							//set root pntr
						}
					}
				}
			}
		 }
		 if (node.leaf) {
			 if(node.n < node.t) {
				insert(student); //again, wtf is this
				student = null;
			 }
		 }
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
    	
    	// "delete" from empty tree ;)
    	if(node == null) {
    		return false;
    	}
    	
    	LinkedList<BTreeNode> parent_stack = new LinkedList<BTreeNode>();
    	LinkedList<Integer> index_stack = new LinkedList<Integer>();

    	// search for leaf node and track path
    	while(!node.leaf) {
    		for(int child = 0; child < node.n; child++) {
    			if(studentId < node.keys[child]) {
    				node = node.children[child];
    	    		parent_stack.push(node);
    				index_stack.push(child);
    				break;
    			}
    			else if(studentId == node.keys[child] || child + 1 == node.keys.length) {
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
    		}
    	}
    	
    	// update nodes along path
    	if(found) {
    		while(!parent_stack.isEmpty()) {
    			BTreeNode parent = parent_stack.pop();
    			int index = index_stack.pop();
    			deleteFromNode(parent, index);
    			if(parent.children[index].n < parent.t) {
    				fill(parent, index);
    			}
    		}
    		// delete removed student from the csv file
    		deleteFromFile("Student.csv", studentId);
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
    			BTreeNode child = node.children[index];
    			BTreeNode predecessor = getPred(child);
    			node.keys[index] = predecessor.keys[0];
    			deleteFromNode(predecessor, 0);
    		} else if(node.children[index + 1].n >= t) {
    			BTreeNode child = node.children[index + 1];
    			BTreeNode successor = getSucc(child);
    			node.keys[index] = successor.keys[successor.n - 1];
    			deleteFromNode(successor, successor.n);
    		} else {
    			merge(node, index);
    			deleteFromNode(node, index);
    		}
    	}
    }
    
    public BTreeNode getSucc(BTreeNode node) {
    	BTreeNode curr = node;
    	while(!curr.leaf) {
    		curr = curr.children[0];
    	}
    	return curr;
    }

    public BTreeNode getPred(BTreeNode node) {
    	BTreeNode curr = node;
    	while(!curr.leaf) {
    		curr = curr.children[curr.n];
    	}
    	return curr;
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
	
	private void split(BTreeNode node, int index) {
		//
	}
    
    public void fill(BTreeNode node, int index) {
    	if(index != 0 && node.children[index - 1].n >= t) {
    		borrowFromPrev(node, index);
    	} else if(index != node.n && node.children[index + 1].n >= t) {
    		borrowFromNext(node, index);
    	} else {
    		if(index != node.n) {
    			merge(node, index);
    		} else {
    			merge(node, index - 1);
    		}
    	}
    }
    
    public void borrowFromPrev(BTreeNode node, int index) {
    	BTreeNode child = node.children[index];
    	BTreeNode sib = node.children[index - 1];
    	
    	for(int i = child.n - 1; i >= 0; i--) {
    		child.keys[i + 1] = child.keys[i];
    		if(child.leaf) {
    			child.values[i + 1] = child.values[i];
    		} else {
    			child.children[i + 1] = child.children[i];
    		}
    	}
    	child.keys[0] = node.keys[index - 1];
    	if(child.leaf) {
    		child.values[0] = node.values[index - 1];
    	} else {
    		child.children[0] = sib.children[sib.n];
    	}
    	child.n += 1;
    	sib.n -= 1;
    }
    
    public void borrowFromNext(BTreeNode node, int index) {
    	BTreeNode child = node.children[index];
    	BTreeNode sib = node.children[index + 1];
    	
    	child.keys[child.n] = node.keys[index];
    	if(child.leaf) {
    		child.values[child.n] = node.keys[index];
    	} else {
    		child.children[child.n + 1] = sib.children[0];
    	}
    	
    	node.keys[index] = sib.keys[0];
    	
    	for(int i = 1; i < sib.n; i++) {
    		sib.keys[i - 1] = sib.keys[i];
    		if(sib.leaf) {
    			sib.values[i - 1] = sib.values[i];
    		} else {
    			sib.children[i - 1] = sib.children[i];
    		}
    	}
    	
    	child.n += 1;
    	sib.n -= 1;
    }
    
    public void deleteFromFile(String csv, long key) {
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
	
	public void insertToFile(String csv, Student s) {
		File file = new File(csv);
		FileWriter fw = null;
		BufferedWriter bw = null;

		try {
			fw = new FileWriter(file);
			bw = new BufferedWriter(fw);
			PrintWriter pw = new PrintWriter(bw);
			
			String entry = s.studentId+","+s.age+","+s.studentName+","+s.major+","+s.level+","+s.recordId;

			pw.println(entry);
			pw.close();
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
    
    List<Long> print() {
        /**
         * Return a list of recordIDs from left to right of leaf nodes.
         */

        List<Long> listOfRecordID = new ArrayList<>();

        BTreeNode cur = getSucc(root);
        do
        {
        	for (long i : cur.values)
        	{
        		if (i == 0) continue;
        		listOfRecordID.add(i);
        	}
        	cur = cur.next;        	
        }
        while (cur.next != null);
        
        return listOfRecordID;
    }
}
