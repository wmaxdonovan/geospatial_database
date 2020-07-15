import java.io.File;
import java.io.FileNotFoundException;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Scanner;
import java.lang.Math;

import com.sun.xml.internal.bind.v2.runtime.unmarshaller.XsiNilLoader.Array;

/**
 * Main Application.
 * <p>
 * You do not need to change this class.
 */
public class BTreeMain {
	
	private static long recordIndex;

    public static void main(String[] args) {

        /** Read the input file -- input.txt */
        Scanner scan = null;
        try {
            scan = new Scanner(new File("input.txt"));
        } catch (FileNotFoundException e) {
            System.out.println("File not found.");
        }

        /** Read the minimum degree of B+Tree first */

        int degree = scan.nextInt();

        BTree bTree = new BTree(degree);

        /** Reading the database student.csv into B+Tree Node*/
        List<Student> studentsDB = getStudents();

        for (Student s : studentsDB) {
            bTree.insert(s);
            recordIndex = Math.max(recordIndex, s.recordId);
        }

        /** Start reading the operations now from input file*/
        try {
            while (scan.hasNextLine()) {
                Scanner s2 = new Scanner(scan.nextLine());

                while (s2.hasNext()) {

                    String operation = s2.next();

                    switch (operation) {
                        case "insert": {

                            long studentId = Long.parseLong(s2.next());
                            String studentName = s2.next() + " " + s2.next();
                            String major = s2.next();
                            String level = s2.next();
                            int age = Integer.parseInt(s2.next());
                            long recordID = ++recordIndex;

                            Student s = new Student(studentId, age, studentName, major, level, recordID);
                            bTree.insert(s);

                            break;
                        }
                        case "delete": {
                            long studentId = Long.parseLong(s2.next());
                            boolean result = bTree.delete(studentId);
                            if (result)
                                System.out.println("Student deleted successfully.");
                            else
                                System.out.println("Student deletion failed.");

                            break;
                        }
                        case "search": {
                            long studentId = Long.parseLong(s2.next());
                            long recordID = bTree.search(studentId);
                            if (recordID != -1)
                                System.out.println("Student exists in the database at " + recordID);
                            else
                                System.out.println("Student does not exist.");
                            break;
                        }
                        case "print": {
                            List<Long> listOfRecordID = new ArrayList<>();
                            listOfRecordID = bTree.print();
                            System.out.println("List of recordIDs in B+Tree " + listOfRecordID.toString());
                        }
                        default:
                            System.out.println("Wrong Operation");
                            break;
                    }
                }
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    private static List<Student> getStudents() {
        List<Student> studentList = new ArrayList<>();
        
        Scanner studentScan = null;
        try {
        	studentScan = new Scanner(new File("Student.csv"));
            studentScan.useDelimiter("\n");
        }
        catch (FileNotFoundException e) {
            System.out.println("File not found.");
        }
        
        while (studentScan.hasNext())
        {
        	String[] line = studentScan.nextLine().split(",");
        	Student s = new Student(
        		Long.parseLong(line[0]),
        		Integer.parseInt(line[4]),
        		line[1],
        		line[2],
        		line[3],
        		Long.parseLong(line[5])
        	);
        	studentList.add(s);
        }
        studentScan.close();
        
        return studentList;
    }
}
