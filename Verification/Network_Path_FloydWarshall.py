//https://rosettacode.org/wiki/Floyd-Warshall_algorithm#C
//https://www.tutorialspoint.com/compile_java_online.php
import static java.lang.String.format;
import java.util.Arrays;
 
public class FloydWarshall {
 
    public static void main(String[] args) {
        int[][] weights = {{1,2,86},{1, 3, 46},{1,4,20}, {2, 1, 100}, {2, 3, 54},{2,4,0},{4,1,61},{4,2,63},{4,3,56},{3, 1,61},{3, 2, 62},{3,4,56}};
        int numVertices = 4;
 
        floydWarshall(weights, numVertices);
    }
 
    static void floydWarshall(int[][] weights, int numVertices) {
 
        double[][] dist = new double[numVertices][numVertices];
        for (double[] row : dist)
            Arrays.fill(row, Double.POSITIVE_INFINITY);
 
        for (int[] w : weights)
            dist[w[0] - 1][w[1] - 1] = w[2];
 
        int[][] next = new int[numVertices][numVertices];
        for (int i = 0; i < next.length; i++) {
            for (int j = 0; j < next.length; j++)
                if (i != j)
                    next[i][j] = j + 1;
        }
 
        for (int k = 0; k < numVertices; k++)
            for (int i = 0; i < numVertices; i++)
                for (int j = 0; j < numVertices; j++)
                    if (dist[i][k] + dist[k][j] < dist[i][j]) {
                        dist[i][j] = dist[i][k] + dist[k][j];
                        next[i][j] = next[i][k];
                    }
 
        printResult(dist, next);
    }
 
    static void printResult(double[][] dist, int[][] next) {
        String siteu="";
        String sitev="";
        System.out.println("Sites lagend: GIST=1,UM=2,HUST=3,CHULA=4");
        System.out.println();
        System.out.println("Sites_pair     Throughput_distance    Path");
        
        for (int i = 0; i < next.length; i++) {
            for (int j = 0; j < next.length; j++) {
                if (i != j) {
                    int u = i + 1;
                    int v = j + 1;
                    if(u==1)
                    siteu="GIST";
                    else if(u==2)
                    else if(u==3)
                    siteu="HUST";
                    else if(u==4)
                    siteu="CHULA";
                    if(v==1)
                    sitev="GIST";
                    else if(v==2)
                    sitev="UM";
                    else if(v==3)
                    sitev="HUST";
                    else if(v==4)
                    sitev="CHULA";
                    
                    String path = format("  %d -> %d             %2d               %s", u, v,
                            (int) dist[i][j], u);
                    do {
                        u = next[u - 1][v - 1];
                        path += " -> " + u;
                    } while (u != v);
                    System.out.println(/*siteu+"->"+sitev+*/path);
                }
            }
        }
    }
}