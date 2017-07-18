package com.example.testing.testapp;

import android.app.Activity;
import android.content.Intent;
import android.content.SharedPreferences;
import android.nfc.NfcAdapter;
import android.support.v4.widget.SwipeRefreshLayout;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.webkit.WebChromeClient;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;
import android.widget.Toast;

public class MainActivity extends AppCompatActivity {

    WebView myWebView;
    SwipeRefreshLayout mySwipeRefreshLayout;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        //Log.d("baygon", "entered onCreate()");
        setContentView(R.layout.activity_main);

        mySwipeRefreshLayout = (SwipeRefreshLayout)this.findViewById(R.id.swipeContainer);
        mySwipeRefreshLayout.setColorSchemeResources(android.R.color.holo_blue_dark);

        myWebView = (WebView) findViewById(R.id.webview);
        myWebView.setWebChromeClient(new WebChromeClient());
        myWebView.setWebViewClient(new WebViewClient(){
            @Override
            public void onPageFinished(WebView view, String url){
                super.onPageFinished(myWebView, url);
                mySwipeRefreshLayout.setRefreshing(false);
            }
        });
        myWebView.getSettings().setJavaScriptEnabled(true);
        myWebView.getSettings().setJavaScriptCanOpenWindowsAutomatically(true);
        myWebView.getSettings().setDomStorageEnabled(true);
        myWebView.getSettings().setDatabaseEnabled(true);
        myWebView.getSettings().setAllowContentAccess(true);
    }

    // upon detecting new intent from NFC tag, if app activity is already running, load the URL from tag in the WebView
    @Override
    protected void onNewIntent(Intent intent){
        super.onNewIntent(intent);
        setIntent(intent);
    }

    @Override
    protected void onResume(){
        super.onResume();
        //Log.d("baygon", "entered onResume()");
        Intent intent = getIntent();
        if(intent!=null && NfcAdapter.ACTION_NDEF_DISCOVERED.equals(intent.getAction())){
            Log.d("baygon", String.valueOf(intent.getData()));
            myWebView.loadUrl(String.valueOf(intent.getData()));
            Toast.makeText(getApplicationContext(), "NFC tag detected", Toast.LENGTH_SHORT).show();
        }
        else {
            myWebView.loadUrl("http://13.228.71.150:8000");
        }

        mySwipeRefreshLayout.setOnRefreshListener(
            new SwipeRefreshLayout.OnRefreshListener(){
                @Override
                public void onRefresh(){
                    //Log.d("baygon", "entered onRefresh()");
                    myWebView.reload();
                }
             }
        );
    }

//    @Override
//    protected void onStop(){
//        super.onStop();
//        Log.d("baygon", "entered onStop()");
//    }
//
//    @Override
//    protected void onDestroy(){
//        super.onDestroy();
//        Log.d("baygon", "entered onDestroy()");
//    }
}
