package bgapps.beny;

import java.io.File;
import java.io.FileInputStream;

import org.apache.http.HttpResponse;
import org.apache.http.client.HttpClient;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.entity.InputStreamEntity;
import org.apache.http.impl.client.DefaultHttpClient;

import android.net.Uri;
import android.os.Bundle;
import android.app.Activity;
import android.content.Intent;
import android.util.Log;
import android.view.Menu;
import android.view.View;
import android.widget.Button;

public class MainActivity extends Activity {

    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        
        Intent intent = getIntent();
        String action = intent.getAction();
        String type = intent.getType();
        
        if (Intent.ACTION_SEND.equals(action) && type != null) {
            if ("application/pdf".equals(type)) {
            	Log.i(MainActivity.class.getName(), action);
            	Uri pdfFileName = intent.getParcelableExtra(Intent.EXTRA_STREAM);
            	File pdfFile = new File(pdfFileName.getPath());
            	
            	try {
            	    HttpClient httpclient = new DefaultHttpClient();

            	    HttpPost httppost = new HttpPost("https://benybgu.appspot.com/upload");

            	    /*InputStreamEntity reqEntity = new InputStreamEntity(
            	            new FileInputStream(pdfFile), -1);
            	    reqEntity.setContentType("binary/octet-stream");
            	    reqEntity.setChunked(true); // Send in multiple parts if needed
            	    httppost.setEntity(reqEntity);
            	    HttpResponse response = httpclient.execute(httppost);*/
            	    //Do something with response...

            	} catch (Exception e) {
            	    // show error
            	}
            } else if ("text/plain".equals(type)) {
            	// TODO handle dropbox shares
            }
        }
        
        final Button button = (Button) findViewById(R.id.btnSend);
        button.setOnClickListener(new View.OnClickListener() {
            public void onClick(View v) {
                // Perform action on click
            }
        });
    }

    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        getMenuInflater().inflate(R.menu.activity_main, menu);
        return true;
    }
}
