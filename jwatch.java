import java.awt.*;
import java.awt.event.*;
import javax.swing.*;
import java.util.*;
import java.text.*;
import java.io.*;

class jwatch extends Thread implements ActionListener {
  public static void main(String args[]) {
    jwatch obj = new jwatch(args);
  }

  String cmd[] = null;
  JFrame frame = null;
  JTextArea pane = null;
  SimpleDateFormat dateFormatter = new SimpleDateFormat("yyyy/MM/dd HH:mm:ss.SSS z");
  JButton button = null;
  boolean paused = false;

  jwatch(String args[]) {
    if (args.length != 1) {
       System.err.println("Syntax: java jwatch 'cmd args...'");
       System.exit(1);
    }
    cmd = new String[3];
    cmd[0] = "bash";
    cmd[1] = "-c";
    cmd[2] = args[0];

    debug("creating frame");
    frame = new JFrame(args[0]);   
    frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);

    pane = new JTextArea();
    pane.setFont(new Font("Monospaced", Font.PLAIN, 15));
    pane.setEditable(false);
    
    button = new JButton("Pause");
    button.addActionListener(this);
    
    frame.getContentPane().setLayout(new BorderLayout());
    frame.getContentPane().add(new JScrollPane(pane), BorderLayout.CENTER);
    frame.getContentPane().add(button, BorderLayout.SOUTH);

    start();
  }

  String now() {
    return dateFormatter.format(new Date());
  }

  void debug(String msg) {
    System.out.println(now() + ": " + msg);
  }

  String join(String strings[]) {
    StringBuffer ret = new StringBuffer();
    for (int i=0; i<strings.length; i++) {
      if (ret.length() > 0)
        ret.append(" ");
      ret.append(strings[i]);
    }
    return ret.toString();
  }

  String read(InputStream stream) {
    StringBuffer ret = new StringBuffer();
    int c;
    boolean done = false;
    while (!done) {
      try {
        c = stream.read();
        if (c != -1) {
          ret.append((char) c);
        }
        else {
          done = true;
        }
      }
      catch (IOException e) {
        debug("read() caught " + e);
        done = true;
      }
    }
    return ret.toString();
  }

  public void run() {
    debug("thread starting");
    while (true) {
      try {
        if (!paused) {
          debug("Running: `" + join(cmd) + "`");
          Process p = Runtime.getRuntime().exec(cmd);
          String text = read(p.getInputStream()) + read(p.getErrorStream());
          pane.setText(text);
  
          int rc = p.waitFor();
          if (!frame.isVisible()) {
            int rows = 1;
            int maxcols = 0;
            int col = 0;
            for (int curr=0; curr < text.length(); curr++) {
              if (text.charAt(curr) == '\n') {
                rows++;
                col = 0;
              }
              else {
                col++;
                if (col > maxcols) maxcols = col;
              }
            }
  
            if (rows < 5) {
              rows = 5;
            }
            else if (rows > 25) {
              rows = 25;
            }
  
            if (maxcols < 25) {
              maxcols = 25;
            }
            else if (maxcols > 80) {
              maxcols = 80;
            }
  
            debug("rows=" + rows + ", cols=" + maxcols);

            pane.setRows(rows);
            pane.setColumns(maxcols);
            frame.pack();
            debug("making frame visible");
            frame.setVisible(true);
          }
        }
        else {
          debug("paused...");
        }

        sleep(5000);
      }
      catch (IOException e) {
        debug("caught " + e);
      }
      catch (InterruptedException e) {
        debug("caught " + e);
      }
    }
  }

  public void actionPerformed(ActionEvent e) {
    if (paused) {
      button.setText("Pause");
    }
    else {
      button.setText("Resume");
    }   
    paused = !paused;
  }
}
