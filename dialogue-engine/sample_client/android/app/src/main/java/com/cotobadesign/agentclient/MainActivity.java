//
//  COTOBA-Agent_sample
//
//  Created by COTOTBA design on Jun 23,2020.
//  Copyright © 2020 COTOTBA design. All rights reserved.
//
package com.cotobadesign.agentclient;

import android.Manifest;
import android.annotation.SuppressLint;
import android.app.AlertDialog;
import android.content.DialogInterface;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.graphics.Color;
import android.graphics.drawable.Drawable;
import android.net.Uri;
import android.os.Build;
import android.os.Handler;
import android.os.Message;
import android.provider.Settings;
import android.speech.RecognitionListener;
import android.speech.RecognizerIntent;
import android.speech.SpeechRecognizer;
import android.speech.tts.TextToSpeech;
import android.speech.tts.UtteranceProgressListener;
import android.support.v4.app.ActivityCompat;
import android.support.v4.content.ContextCompat;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.ListView;
import android.widget.Toast;

import java.util.ArrayList;
import java.util.HashMap;

import butterknife.BindDrawable;
import butterknife.BindView;
import butterknife.ButterKnife;

public class MainActivity extends AppCompatActivity implements TextToSpeech.OnInitListener{
    private static final String TAG = "COTOBA_Agent";
    private static final int MSG_RECOG = 1;
    private static final int MSG_DIALOG = 2;
    private static final int MSG_TTS = 3;
    private static final int MSG_SCROLL = 4;
    private final static String MSG_RECOG_OBJ = "RetryRecognition";
    private final static String MSG_SCROLL_OBJ = "ViewScroll";
    private SpeechRecognizer mSr;
    private TextToSpeech mTts;
    private boolean mRecognizeState;
    private boolean mRecognizeRestart;
    private CommentAdapter mAdapter;
    private ArrayList<Comment> commentArrayList = new ArrayList<Comment>();


    @BindView(R.id.ChatView) ListView mChatView;
    @BindDrawable(R.drawable.face1) Drawable botDrawable;
    @BindDrawable(R.drawable.face2) Drawable userDrawable;
    @BindView(R.id.StartBtn) Button mStartButton;
    @BindDrawable(R.drawable.style_green) Drawable greenButton;
    @BindDrawable(R.drawable.style_red) Drawable redButton;


    private void displayString( int aId, String aString) {
        Drawable drawable = (aId == 1) ?  botDrawable : userDrawable;
        commentArrayList.add(new Comment(aId, drawable, aString));
        mAdapter = new CommentAdapter(this, 1, commentArrayList);
        mChatView.setAdapter(mAdapter);
        mChatView.setSelection(mAdapter.getCount());
    }


    @SuppressLint("HandlerLeak")
    private final Handler mAppHandler = new Handler() {
        @Override
        public void handleMessage(Message msg) {
            String messageObj = (String) msg.obj;
            switch (msg.what) {
                case MSG_RECOG:
                    mChatView.setSelection(mAdapter.getCount());
                    if(mRecognizeRestart){
                        restartListeningService();
                    }else{
                        stopListening();
                        mStartButton.setText(R.string.start_button);
                        mStartButton.setBackground(greenButton);
                    }
                    break;
                case MSG_DIALOG:
                    displayString(2, messageObj );
                    mAppHandler.sendMessage(mAppHandler.obtainMessage(MSG_TTS, messageObj));
                    break;
                case MSG_TTS:
                    speechText(messageObj);
                    break;
                case MSG_SCROLL:
                    mChatView.setSelection(mAdapter.getCount());
                    break;
            }
        }
    };

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        ButterKnife.bind(this);
        checkAudioPermission();

        mRecognizeState = false;
        mRecognizeRestart = false;
        mStartButton.setTextColor(Color.WHITE);
        mStartButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {

                if( mRecognizeState ){
                    Log.d(TAG,"Stop Recognition");
                    mStartButton.setText(R.string.start_button);
                    mStartButton.setBackground(greenButton);
                    stopListening();
                }else{
                    Log.d(TAG,"Start Recognition");
                    mStartButton.setText(R.string.stop_button);
                    mStartButton.setBackground(redButton);
                    startListening();
                }
            }
        });
    }

    @Override
    protected void onResume() {
        mTts = new TextToSpeech(this,this);
        mStartButton.setText("Start");
        mStartButton.setBackground(greenButton);
        mRecognizeState = false;
        mRecognizeRestart = false;
        super.onResume();
    }

    @Override
    protected void onPause() {
        if( mRecognizeState ){
            mRecognizeState = false;
            stopListening();
        }
        if (null != mTts) {
            // to release the resource of TextToSpeech
            mTts.shutdown();
        }

        super.onPause();
    }

    // Start speech recognition
    protected void startListening() {
        mRecognizeState = true;
        try {
            if (mSr == null) {
                mSr = SpeechRecognizer.createSpeechRecognizer(this);
                if (!SpeechRecognizer.isRecognitionAvailable(getApplicationContext())) {
                    Toast.makeText(getApplicationContext(), "Cannot use speech recognizer",
                            Toast.LENGTH_LONG).show();
                    finish();
                }
                mSr.setRecognitionListener(new listener());
            }
            // インテントの作成
            Intent intent = new Intent(RecognizerIntent.ACTION_RECOGNIZE_SPEECH);
            // 言語モデル指定
            intent.putExtra(RecognizerIntent.EXTRA_LANGUAGE_MODEL,
                    RecognizerIntent.LANGUAGE_MODEL_WEB_SEARCH);
            mSr.startListening(intent);
        } catch (Exception ex) {
            Toast.makeText(getApplicationContext(), "error occur at startListening()",
                    Toast.LENGTH_LONG).show();
            finish();
        }
    }

    // Stop speech recognition
    protected void stopListening() {
        mRecognizeState = false;
        if (mSr != null) mSr.destroy();
        mSr = null;
    }

    // Restart speech recognition
    public void restartListeningService() {
        if( mRecognizeState) {
            stopListening();
            startListening();
        }
    }

    // RecognitionListener
    class listener implements RecognitionListener {
        public void onBeginningOfSpeech() {
        }
        public void onBufferReceived(byte[] buffer) {
        }
        public void onEndOfSpeech() {
        }
        public void onReadyForSpeech(Bundle params) {
        }
        public void onResults(Bundle results) {
            ArrayList results_array = results.getStringArrayList(
                    SpeechRecognizer.RESULTS_RECOGNITION);
            String resultsString = "";
//            for (int i = 0; i < results.size(); i++) {
            {
                int i = 0; // Adopt the first utterance
                resultsString += results_array.get(i);
            }

            Log.d(TAG, "Recognize result:"+resultsString);
            displayString(1,resultsString);

            // Dialogue Request
            getDialoguResult(resultsString);
        }



        public void onError(int error) {
            String reason = "";
            boolean indicate = true;
            switch (error) {
                case SpeechRecognizer.ERROR_AUDIO:
                    reason = "ERROR_AUDIO";
                    break;
                case SpeechRecognizer.ERROR_CLIENT:
                    reason = "ERROR_CLIENT";
                    break;
                case SpeechRecognizer.ERROR_INSUFFICIENT_PERMISSIONS:
                    reason = "ERROR_INSUFFICIENT_PERMISSIONS: Please enable microphone permission";
                    break;
                case SpeechRecognizer.ERROR_NETWORK:
                    reason = "ERROR_NETWORK";
                    break;
                case SpeechRecognizer.ERROR_NETWORK_TIMEOUT:
                    reason = "ERROR_NETWORK_TIMEOUT";
                    break;
                case SpeechRecognizer.ERROR_NO_MATCH:
                    indicate = false;
                    reason = "ERROR_NO_MATCH";
                    break;
                case SpeechRecognizer.ERROR_RECOGNIZER_BUSY:
                    reason = "ERROR_RECOGNIZER_BUSY";
                    break;
                case SpeechRecognizer.ERROR_SERVER:
                    reason = "ERROR_SERVER";
                    break;
                case SpeechRecognizer.ERROR_SPEECH_TIMEOUT:
                    indicate = false;
                    reason = "ERROR_SPEECH_TIMEOUT";
                    break;
            }
            Log.e(TAG, "SpeechRecopgnizer error:" +reason);
            if( indicate ) {
                Toast.makeText(getApplicationContext(), reason, Toast.LENGTH_SHORT).show();
            }
            restartListeningService();

        }
        public void onEvent(int eventType, Bundle params) {
        }
        public void onPartialResults(Bundle partialResults) {
        }
        public void onRmsChanged(float rmsdB) {
        }
    }

    // TTS
    @Override
    public void onInit(int status) {
        // TTS初期化
        if (TextToSpeech.SUCCESS == status) {
            Log.d(TAG, "TTS initialized");
        } else {
            Log.e(TAG, "TTS failed to initialize");
        }
    }

    private void speechText(String aString) {

        if (0 < aString.length()) {
            if (mTts.isSpeaking()) {
                mTts.stop();
                return;
            }

            if (Build.VERSION.SDK_INT >= 21){
                // SDK 21 以上
                mTts.speak(aString, TextToSpeech.QUEUE_FLUSH, null, "messageID");
            }
            else{
                HashMap<String, String> map = new HashMap<String, String>();
                map.put(TextToSpeech.Engine.KEY_PARAM_UTTERANCE_ID,"messageID");
                mTts.speak(aString, TextToSpeech.QUEUE_FLUSH, map);
            }

            setTtsListener();
        }
    }

    // 読み上げの始まりと終わりを取得
    private void setTtsListener(){
        // android version more than 15th
        if (Build.VERSION.SDK_INT >= 15){
            int listenerResult =
                    mTts.setOnUtteranceProgressListener(new UtteranceProgressListener() {
                        @Override
                        public void onDone(String utteranceId) {
                            Log.d(TAG,"progress on Done " + utteranceId);
                            mAppHandler.sendMessage(mAppHandler.obtainMessage(MSG_RECOG, MSG_RECOG_OBJ));
                        }

                        @Override
                        public void onError(String utteranceId) {
                            Log.d(TAG,"progress on Error " + utteranceId);
                        }

                        @Override
                        public void onStart(String utteranceId) {
                            mAppHandler.sendMessage(mAppHandler.obtainMessage(MSG_SCROLL, MSG_SCROLL_OBJ));
                            Log.d(TAG,"progress on Start " + utteranceId);
                        }
                    });

            if (listenerResult != TextToSpeech.SUCCESS) {
                Log.e(TAG, "failed to add utterance progress listener");
            }
        }
        else {
            Log.e(TAG, "Build VERSION is less than API 16");
        }
    }

    private void getDialoguResult(String aUtterance)
    {
        cotobaAgentCall(aUtterance);
        return;
    }

    private void cotobaAgentCall(String aUtterance){
        // NLU call
        CotobaAgentCall cotobaEngine = new CotobaAgentCall();
        cotobaEngine.setListener(createCotobaEngineListener());
        cotobaEngine.setDialogueURL(getResources().getString(R.string.endpointurl));
        cotobaEngine.setUserId(getResources().getString(R.string.userid));
        cotobaEngine.setApiKey(getResources().getString(R.string.api_key));
        cotobaEngine.execute(aUtterance);
    }

    private CotobaAgentCall.Listener createCotobaEngineListener() {
        return new CotobaAgentCall.Listener() {
            @Override
            public void onSuccess(String aResult) {
                String ttsString = aResult;
                if (ttsString.length() <= 0) {
                    ttsString = getResources().getString(R.string.unconnect_dialog);
                    mRecognizeRestart = false;
                }else{
                    mRecognizeRestart = true;
                }

                mAppHandler.sendMessage(mAppHandler.obtainMessage(MSG_DIALOG,  ttsString));
            }
        };
    }

    private static final int REQUEST_AUDIORECORD_PERMISSION = 1;
    private static final String RECOGNIZE_DIALOG = "dialog";


    private void checkAudioPermission() {
        if (ContextCompat.checkSelfPermission(this, Manifest.permission.RECORD_AUDIO)
                != PackageManager.PERMISSION_GRANTED) {
            requestMicrophonePermission();
            return;
        }
    }

    private void requestMicrophonePermission() {


        if (ActivityCompat.shouldShowRequestPermissionRationale(this,
                Manifest.permission.RECORD_AUDIO)) {

            Log.d(TAG, "shouldShowRequestPermissionRationale:Additional explanation");
            // As a result of the authority check, if you do not have it, issue a dialog
            AlertDialog.Builder builder = new AlertDialog.Builder(this);

            builder.setTitle("Additional description of permissions");
            builder.setMessage("Permissions are required to perform speech recognition in this application.");
            builder.setPositiveButton(android.R.string.ok, new DialogInterface.OnClickListener() {
                @Override
                public void onClick(DialogInterface dialog, int which) {
                    ActivityCompat.requestPermissions(MainActivity.this,
                            new String[]{Manifest.permission.RECORD_AUDIO},
                            REQUEST_AUDIORECORD_PERMISSION);
                }
            })
                    .create()
                    .show();
            return;
        }

        // Get permissions
        ActivityCompat.requestPermissions(this, new String[]{
                        Manifest.permission.RECORD_AUDIO
                },
                REQUEST_AUDIORECORD_PERMISSION);
        return;
    }
    private void openSettings() {
        Intent intent = new Intent(Settings.ACTION_APPLICATION_DETAILS_SETTINGS);
        Uri uri = Uri.fromParts("package", getPackageName(), null);
        intent.setData(uri);
        startActivity(intent);
    }


}
