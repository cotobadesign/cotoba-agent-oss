package com.cotobadesign.agentclient;

import android.net.Uri;
import android.os.AsyncTask;
import android.util.Log;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.io.PrintStream;
import java.net.HttpURLConnection;
import java.net.MalformedURLException;
import java.net.ProtocolException;
import java.net.URL;
import java.net.URLEncoder;
import java.util.HashMap;
import java.util.Set;

public class CotobaAgentCall extends AsyncTask<String, Void, String>{
    private static final String TAG = "CotobaEngineCall";

    private String mDialogueUrl;
    private String mUserId;
    private String mApiKey;

    private Listener listener;

    public void setListener(Listener listener) {
        this.listener = listener;
    }

    interface Listener {
        void onSuccess(String aResult);
    }


    // 非同期処理
    @Override
    protected String doInBackground(String... params) {

        return getResponse(params[0]) ;
    }

    @Override
    protected void onProgressUpdate(Void... progress) {
    }

    // 非同期処理が終了後、結果をメインスレッドに返す
    @Override
    protected void onPostExecute(String aResult) {
        if (listener != null) {
            listener.onSuccess(aResult);
        }
    }


    public void setDialogueURL(String aDialogUrl){
        mDialogueUrl = aDialogUrl;
    }
    public void setUserId(String aUserId){
        mUserId = aUserId;
    }

    public void setApiKey(String aApiKey){
        mApiKey = aApiKey;
    }



    private String getResponse(String aUtterance) {
        HttpURLConnection urlConn = null;
        InputStream in = null;
        BufferedReader reader = null;
        String responseText = "";

        try {

            // get Utterance
            String urlString = mDialogueUrl;
            JSONObject requestJson = new JSONObject();
            requestJson.put("utterance", aUtterance);
            requestJson.put("userId", mUserId);

            URL url = new URL(urlString);
            urlConn = (HttpURLConnection) url.openConnection();
            urlConn.setRequestMethod("POST");
            urlConn.setRequestProperty("Content-Type", "application/json;charset=utf-8");
            urlConn.setRequestProperty("x-api-key", mApiKey);
            urlConn.setDoOutput(true);
            OutputStream os = urlConn.getOutputStream();
            PrintStream ps = new PrintStream(os);
            ps.print(requestJson.toString());
            ps.close();

            urlConn.connect();
            int status = urlConn.getResponseCode();
            Log.d(TAG, "http status:" + status);

            if (status == HttpURLConnection.HTTP_OK) {
                in = urlConn.getInputStream();
                reader = new BufferedReader(new InputStreamReader(in));
                StringBuilder output = new StringBuilder();
                String line;
                while ((line = reader.readLine()) != null) {
                    output.append(line);
                }
                Log.d(TAG, "reg:get content:" + output.toString());

                JSONObject json = new JSONObject(output.toString());
                responseText = json.getString("response");
                Log.d("responseText:", responseText);
            } else {
                Log.e(TAG, "HTTP ERROR:" + status);
            }
        } catch (JSONException e) {
            e.printStackTrace();
        } catch (MalformedURLException e) {
            e.printStackTrace();
        } catch (ProtocolException e) {
            e.printStackTrace();
        } catch (IOException e) {
            e.printStackTrace();
        } catch (Exception e) {
            e.printStackTrace();
        } finally {
            try {
                if (reader != null) {
                    reader.close();
                }
                if (urlConn != null) {
                    urlConn.disconnect();
                }
            } catch (IOException e) {
                e.printStackTrace();
            }
        }

        return responseText;
    }
}
