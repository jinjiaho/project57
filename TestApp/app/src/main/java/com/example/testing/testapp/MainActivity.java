package com.example.testing.testapp;

import android.annotation.SuppressLint;
import android.app.Activity;
import android.content.Intent;
import android.net.Uri;
import android.nfc.NfcAdapter;
import android.os.Environment;
import android.os.Handler;
import android.provider.MediaStore;
import android.support.v4.widget.SwipeRefreshLayout;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.webkit.DownloadListener;
import android.webkit.ValueCallback;
import android.webkit.WebChromeClient;
import android.webkit.WebView;
import android.webkit.WebViewClient;
import android.widget.Toast;

import java.io.File;
import java.io.IOException;
import java.text.SimpleDateFormat;
import java.util.Date;

import static android.provider.MediaStore.ACTION_IMAGE_CAPTURE;

public class MainActivity extends AppCompatActivity {

    WebView myWebView;
    SwipeRefreshLayout mySwipeRefreshLayout;

    // If want to add back function for the app, use this code
//    private boolean doubleBackToExitPressedOnce;
//    private Handler mHandler = new Handler();

    private static final String TAG = MainActivity.class.getSimpleName();
    private String mCM;
    private ValueCallback<Uri[]> mUMA;
    private final static int FCR = 1;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        mySwipeRefreshLayout = (SwipeRefreshLayout)this.findViewById(R.id.swipeContainer);
        mySwipeRefreshLayout.setColorSchemeResources(android.R.color.holo_blue_dark);

        myWebView = (WebView) findViewById(R.id.webview);

        myWebView.setWebViewClient(new WebViewClient(){
            @Override
            public void onPageFinished(WebView view, String url){
                super.onPageFinished(myWebView, url);
                mySwipeRefreshLayout.setRefreshing(false);
            }
        });

        myWebView.setWebChromeClient(new WebChromeClient(){
            public boolean onShowFileChooser(WebView webView, ValueCallback<Uri[]> filePathCallback, WebChromeClient.FileChooserParams fileChooserParams){
                if(mUMA != null){
                    mUMA.onReceiveValue(null);
                }
                mUMA = filePathCallback;
                Intent takePictureIntent = new Intent(ACTION_IMAGE_CAPTURE);
                if(takePictureIntent.resolveActivity(MainActivity.this.getPackageManager()) != null){
                    File photoFile = null;
                    try{
                        photoFile = createImageFile();
                        takePictureIntent.putExtra("PhotoPath", mCM);
                    }
                    catch(IOException ex){
                        Log.e(TAG, "Image file creation failed", ex);
                    }
                    if(photoFile != null){
                        mCM = "file:" + photoFile.getAbsolutePath();
                        takePictureIntent.putExtra(MediaStore.EXTRA_OUTPUT, Uri.fromFile(photoFile));
                    }
                    else{
                        takePictureIntent = null;
                    }
                }

                Intent contentSelectionIntent = new Intent(Intent.ACTION_GET_CONTENT);
                contentSelectionIntent.addCategory(Intent.CATEGORY_OPENABLE);
                contentSelectionIntent.setType("*/*");
                Intent[] intentArray;
                if(takePictureIntent != null){
                    intentArray = new Intent[]{takePictureIntent};
                }
                else{
                    intentArray = new Intent[0];
                }

                Intent chooserIntent = new Intent(Intent.ACTION_CHOOSER);
                chooserIntent.putExtra(Intent.EXTRA_INTENT, contentSelectionIntent);
                chooserIntent.putExtra(Intent.EXTRA_TITLE, "Image Chooser");
                chooserIntent.putExtra(Intent.EXTRA_INITIAL_INTENTS, intentArray);
                startActivityForResult(chooserIntent, FCR);
                return true;
            }
        });

        myWebView.getSettings().setJavaScriptEnabled(true);
        myWebView.getSettings().setJavaScriptCanOpenWindowsAutomatically(true);
        myWebView.getSettings().setDomStorageEnabled(true);
        myWebView.getSettings().setDatabaseEnabled(true);

        // load whichever URL the webapp has
        //myWebView.loadUrl("http://13.228.71.150:80");
        myWebView.loadUrl("http://ec2-52-77-253-63.ap-southeast-1.compute.amazonaws.com");
    }

    @Override
    protected void onNewIntent(Intent intent){
        super.onNewIntent(intent);
        setIntent(intent);
    }

    @Override
    protected void onResume(){
        super.onResume();
        Intent intent = getIntent();
        if(intent!=null && NfcAdapter.ACTION_NDEF_DISCOVERED.equals(intent.getAction())){
            myWebView.loadUrl(String.valueOf(intent.getData()));
            Toast.makeText(getApplicationContext(), "NFC tag detected", Toast.LENGTH_SHORT).show();
        }

        mySwipeRefreshLayout.setOnRefreshListener(
                new SwipeRefreshLayout.OnRefreshListener(){
                    @Override
                    public void onRefresh(){
                        myWebView.reload();
                    }
                }
        );
    }

    @Override
    protected void onActivityResult(int requestCode, int resultCode, Intent intent){
        super.onActivityResult(requestCode, resultCode, intent);

        Uri[] results = null;
        if(resultCode == Activity.RESULT_OK){
            if(requestCode == FCR){
                if(null == mUMA){
                    return;
                }
                if(intent == null){
                    if(mCM != null){
                        results = new Uri[]{Uri.parse(mCM)};
                    }
                }
                else{
                    String dataString = intent.getDataString();
                    if(dataString != null){
                        results = new Uri[]{Uri.parse(dataString)};
                    }
                }
            }
        }
        mUMA.onReceiveValue(results);
        mUMA = null;
    }

    private File createImageFile() throws IOException{
        @SuppressLint("SimpleDateFormat") String timeStamp = new SimpleDateFormat("yyyyMMdd_HHmmss").format(new Date());
        String imageFileName = "img_" + timeStamp + "_";
        File storageDir = Environment.getExternalStoragePublicDirectory(Environment.DIRECTORY_PICTURES);
        return File.createTempFile(imageFileName, ".jpg", storageDir);
    }

    // If want to add back function for the app, use this code

//    private final Runnable mRunnable = new Runnable() {
//        @Override
//        public void run() {
//            doubleBackToExitPressedOnce = false;
//        }
//    };
//
//    @Override
//    protected void onDestroy(){
//        super.onDestroy();
//
//        if(mHandler != null){
//            mHandler.removeCallbacks(mRunnable);
//        }
//    }
//
//    @Override
//    public void onBackPressed(){
//        if(myWebView.canGoBack()){
//            myWebView.goBack();
//            //myWebView.reload();
//        }
//        else{
//            if(doubleBackToExitPressedOnce){
//                super.onBackPressed();
//                return;
//            }
//
//            this.doubleBackToExitPressedOnce = true;
//            Toast.makeText(this, "Please press back again to exit", Toast.LENGTH_SHORT).show();
//
//            mHandler.postDelayed(mRunnable, 2000);
//        }
//    }
}
