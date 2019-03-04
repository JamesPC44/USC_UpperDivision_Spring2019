import java.util.*;

public class Solution {

  public static void main(String[] args) {
    Scanner in = new Scanner(System.in);
    int objcount = in.nextInt();
    int[] arr = new int[objcount];
    for (int n = 0; n < objcount; n++) {
      arr[n] = in.nextInt();
    }
    in.close();
    int res = 0;
    for (int mask = 1 << 30; mask > 0; mask >>= 1) {
      if (!qsorted(arr, mask - 1)) {
        for (int i = 0; i < arr.length; i++) {
          arr[i] |= mask;
        }
        res |= mask;
      }
    }
    System.out.println(res);
  }

  public static boolean qsorted(int[] arr, int mask) {
    for (int i = 0; i < arr.length - 1; i++) {
      if ((arr[i] | mask) > (arr[i + 1] | mask)) {
        return false;
      }
    }
    return true;
  }
}
