import java.io.*;
import java.util.*;
import java.text.*;
import java.math.*;
import java.util.regex.*;

public class Solution {

     public static void main(String[] args) {
    Scanner in = new Scanner(System.in);
    int objcount = in.nextInt();
    int[] arr = new int[objcount];
    int[] arr2 = new int[objcount];
    for (int n = 0; n < objcount; n++) {
      arr[n] = in.nextInt();
      arr2[n] = arr[n];
    }
    in.close();
    int mask = 0;
    int res = 0;
    while (!qsorted(arr, mask)) {
      mask++;
    }
    // System.out.println(mask);
    while (mask >= 0) {
     // System.out.println("m " + mask);
      if (!qsorted(arr, mask)) {
        applymask(arr, mask);
        //pa(arr);
        res |= 1 << mask;
      }

      //System.out.println("r " + res);
      mask--;
    }
    
    // comment out to disable fast solution
    
    System.out.println(res);

    // uncomment to enable naive solution
    
    //int res2 = 0;
    //while (!check(arr2, res2)) {
    //  res2++;
    //}
    //System.out.println(res2);
  }

  public static void pa(int[] arr) {
    for (int i = 0; i < arr.length; i++) {
      System.out.println(" " + arr[i]);
    }
  }

  public static String gencase(int[] arr) {
    String res = "";
    res += arr.length + String.format("%n");
    for (int i = 0; i < arr.length; i++) {
      res += arr[i] + String.format("%n");
    }
    return res;
  }

  public static boolean qsorted(int[] arr, int m) {
    int mask = (1 << m) - 1;
    int max = 0;
    for (int i = 0; i < arr.length; i++) {
      if ((arr[i] | mask) < max) {
        return false;
      }
      max = arr[i] | mask;
    }
    return true;
  }

  public static boolean check(int[] arr, int mask) {
    int max = 0;
    for (int i = 0; i < arr.length; i++) {
      if ((arr[i] | mask) < max) {
        return false;
      }
      max = arr[i] | mask;
    }
    return true;
  }

  public static void applymask(int[] arr, int m) {
    int mask = 1 << m;
    for (int i = 0; i < arr.length; i++) {
      arr[i] |= mask;
    }
  }
}
