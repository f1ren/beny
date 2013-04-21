package bgapps.beny;

import java.io.DataOutputStream;
import java.io.File;
import java.io.FileInputStream;
import java.io.IOException;
import java.net.HttpURLConnection;
import java.net.URL;

import org.apache.http.HttpResponse;
import org.apache.http.client.ClientProtocolException;
import org.apache.http.client.HttpClient;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.entity.InputStreamEntity;
import org.apache.http.entity.mime.MultipartEntity;
import org.apache.http.entity.mime.content.FileBody;
import org.apache.http.entity.mime.content.StringBody;
import org.apache.http.impl.client.DefaultHttpClient;

import android.net.Uri;
import android.os.Bundle;
import android.app.Activity;
import android.content.Intent;
import android.util.Log;
import android.view.Menu;
import android.view.View;
import android.widget.Button;
import android.widget.Toast;

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
            	Uploader uploader = new Uploader();
            	uploader.upload(getApplicationContext(), pdfFileName.getPath());
            } else if ("text/plain".equals(type)) {
            	// TODO handle dropbox shares
            }
        }
        
        final Button button = (Button) findViewById(R.id.btnSend);
        button.setOnClickListener(new View.OnClickListener() {
            public void onClick(View v) {
            	Uploader uploader = new Uploader();
            	uploader.upload(MainActivity.this, "/sdcard/sol5.pdf");
            }
        });
    }

    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        getMenuInflater().inflate(R.menu.activity_main, menu);
        return true;
    }
}
