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
    for (int n = 0; n < objcount; n++) {
      arr[n] = in.nextInt();
    }
    in.close();
    int mask = 0;
    int res = 0;
    while (!qsorted(arr, (1 << mask) - 1)) {
      mask++;
    }
    while (mask >= 0) {
      if (!qsorted(arr, (1 << mask) - 1)) {
        applymask(arr, 1 << mask);
        res |= 1 << mask;
      }
      mask--;
    }
    System.out.println(res);
  }

  public static boolean qsorted(int[] arr, int m) {
    int max = 0;
    for (int i = 0; i < arr.length; i++) {
      if ((arr[i] | m) < max) {
        return false;
      }
      max = arr[i] | m;
    }
    return true;
  }

  public static void applymask(int[] arr, int m) {
    for (int i = 0; i < arr.length; i++) {
      arr[i] |= m;
    }
  }
}
