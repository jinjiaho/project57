package com.example.testing.testapp;

import android.content.Intent;
import android.nfc.NfcAdapter;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.KeyEvent;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;

public class MainActivity extends AppCompatActivity {
    WebView myWebView;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        // get reference to the WebView
        myWebView = (WebView) findViewById(R.id.webview);

        // enable JavaScript
        WebSettings webSettings = myWebView.getSettings();
        webSettings.setJavaScriptEnabled(true);

        // open webpage inside WebView
        myWebView.setWebViewClient(new WebViewClient());

        // specify URL to load on app launch
        myWebView.loadUrl("http://13.228.71.150:8000");
    }

    // allows WebView to return to previous webpage instead of previous activity
//    @Override
//    public boolean onKeyDown(final int keyCode, final KeyEvent event){
//        if((keyCode == KeyEvent.KEYCODE_BACK) && myWebView.canGoBack()){
//            myWebView.goBack();
//            // if there is history, .canGoBack() will return true
//            return true;
//        }
//        return super.onKeyDown(keyCode, event);
//    }

    // upon detecting new intent from NFC tag, load the URL from tag in the WebView
    @Override
    protected void onNewIntent(Intent intent){
        super.onNewIntent(intent);
        if(intent!=null && NfcAdapter.ACTION_NDEF_DISCOVERED.equals(intent.getAction())){
            Log.d("baygon", String.valueOf(intent.getData()));
            myWebView.loadUrl(String.valueOf(intent.getData()));
            setIntent(intent);
        }
    }
}
