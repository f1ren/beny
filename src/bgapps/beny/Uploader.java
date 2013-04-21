package bgapps.beny;

import java.io.File;
import java.io.IOException;

import org.apache.http.HttpResponse;
import org.apache.http.client.ClientProtocolException;
import org.apache.http.client.HttpClient;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.entity.mime.MultipartEntity;
import org.apache.http.entity.mime.content.FileBody;
import org.apache.http.entity.mime.content.StringBody;
import org.apache.http.util.EntityUtils;
import org.apache.http.impl.client.DefaultHttpClient;

import android.app.ProgressDialog;
import android.content.Context;
import android.os.AsyncTask;

public class Uploader {
	ProgressDialog dialog;
	public void upload(Context context, String filePath) {
		dialog = ProgressDialog.show(context, "Uploading", "");
		new AsyncPoster().execute(filePath);
	}
    private class AsyncPoster extends AsyncTask<String, Void, String> {
    	@Override protected String doInBackground(String... filePath) {
    		File pdfFile = new File(filePath[0]);
    		String result = "Error";
        	
        	try {
        		HttpClient httpclient = new DefaultHttpClient();
        		HttpPost httppost = new HttpPost("https://benybgu.appspot.com/upload");
        		 
        		try {
        		  MultipartEntity entity = new MultipartEntity();
        		 
        		  entity.addPart("uname", new StringBody("navatm"));
        		  entity.addPart("password", new StringBody("photo"));
        		  entity.addPart("path", new StringBody("???"));
        		  entity.addPart("exnum", new StringBody("1"));
        		  entity.addPart("exercise", new FileBody(pdfFile));
        		  httppost.setEntity(entity);
        		  HttpResponse response = httpclient.execute(httppost);
        		  result = EntityUtils.toString(response.getEntity());
        		} catch (ClientProtocolException e) {
        			result = e.toString();
        		} catch (IOException e) {
        			result = e.toString();
        		}
        	} catch (Exception e) {
        		result = e.toString();
        	}
        	return result;
        }

        @Override protected void onPostExecute(String res) {
        	dialog.dismiss();
        }
    }
}
