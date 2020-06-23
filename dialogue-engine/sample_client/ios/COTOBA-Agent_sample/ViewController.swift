//
//  ViewController.swift
//  COTOBA-Agent_sample
//
//  Created by COTOTBA design on June 23,2020.
//  Copyright © 2020 COTOTBA design. All rights reserved.
//

import UIKit
import AVFoundation
import Speech

class ViewController: UIViewController, AVSpeechSynthesizerDelegate {

    @IBOutlet weak var dialogOutput: UITextView!
    @IBOutlet weak var dialogStartStop: UIButton!
    private let speechRecognizer = SFSpeechRecognizer(locale: Locale(identifier: "ja-JP"))!
    private var recognitionRequest: SFSpeechAudioBufferRecognitionRequest?
    private var recognitionTask: SFSpeechRecognitionTask?
    private let audioEngine = AVAudioEngine()
    private let talker = AVSpeechSynthesizer()
    private let endpointURL = "SET_YOUR_ENDPOINT"
    private let userId = "SET_YOUR_USERID"
    private let apiKey = "SET_YOUR_API_KEY"

    override func viewDidLoad() {
        super.viewDidLoad()
        
        // TTS setup
        self.talker.delegate = self
        
        // STT setup
        requestRecognizerAuthorization()
        
        // Button setup
        dialogStartStop.backgroundColor = UIColor.green
        dialogStartStop.tintColor = UIColor.black
    }
    

    // COTOBA Agent call
    func cotobaCall(url:String, apiKey:String, utterance:String ){
        let request = NSMutableURLRequest(url: NSURL(string: url)! as URL)
        let session = URLSession.shared
        
        request.httpMethod = "POST"
        request.addValue("application/json", forHTTPHeaderField: "Content-Type")
        request.addValue(apiKey, forHTTPHeaderField: "x-api-key")
        
        let json: [String: Any] = ["utterance": utterance,
                                   "userId": userId]
        
        let jsonData = try? JSONSerialization.data(withJSONObject: json)
        request.httpBody = jsonData
        
        let task = session.dataTask(with: request as URLRequest, completionHandler: {data, response, error -> Void in
            if error != nil {
                print("Error: \(String(describing: error))")
                return
            }
            guard let data = data, error == nil else {
                print(error?.localizedDescription ?? "No data")
                return
            }
            let responseJSON = try? JSONSerialization.jsonObject(with: data, options: [])
            if let responseJSON_String = responseJSON as? [String: Any] {
                print(responseJSON_String)
                let response = responseJSON_String["response"]
                print(response as! String)
                DispatchQueue.main.async {
                    self.addText("response:" + (response as! String))
                    self.speechText(response as! String)
                }
            }
            
        })
        
        task.resume()
    }
    
    @IBAction func btnClick(_ sender: UIButton){

        if dialogStartStop.currentTitle == "Start" {
            dialogOutput.text = ""
            try? sttStart()
            dialogStartStop.setTitle("Stop", for: .normal)
            dialogStartStop.backgroundColor = UIColor.red
            dialogStartStop.tintColor = UIColor.white
        }else{
            sttStop()
            dialogStartStop.setTitle("Start", for: .normal)
            dialogStartStop.backgroundColor = UIColor.green
            dialogStartStop.tintColor = UIColor.black
        }
    }
    
    // Text view controll
    func scrollToBottom() {
        dialogOutput.isScrollEnabled = true
        
        let scrollY = dialogOutput.contentSize.height - dialogOutput.bounds.height
        let scrollPoint = CGPoint(x: 0, y: scrollY > 0 ? scrollY : 0)
        dialogOutput.setContentOffset(scrollPoint, animated: true)
    }
    
    func addText(_ text: String) {
        dialogOutput.isScrollEnabled = false
        dialogOutput.text.append("\n" + text)
        scrollToBottom()
    }

    
    // TTS
    func speechText(_ text: String){
        let utterance = AVSpeechUtterance(string: text)
        print(AVSpeechSynthesisVoice.speechVoices())
        utterance.voice = AVSpeechSynthesisVoice(language: "ja-JP")
        utterance.rate = AVSpeechUtteranceDefaultSpeechRate
        
        talker.speak(utterance)
    }
    
    func speechSynthesizer(_ synthesizer: AVSpeechSynthesizer,
                           didFinish utterance: AVSpeechUtterance)
    {
        try? sttStart()
    }

    
    // STT
    private func requestRecognizerAuthorization() {
        SFSpeechRecognizer.requestAuthorization { (authStatus) in
        }
    }

    private func sttStart() throws {
        if let recognitionTask = recognitionTask {
            recognitionTask.cancel()
            self.recognitionTask = nil
        }
        
        let audioSession = AVAudioSession.sharedInstance()
        try audioSession.setCategory(.playAndRecord, mode: .default, options: [])
        try audioSession.setActive(true, options: .notifyOthersOnDeactivation)
        
        let recognitionRequest = SFSpeechAudioBufferRecognitionRequest()
        self.recognitionRequest = recognitionRequest
        recognitionRequest.shouldReportPartialResults = true
        recognitionTask = speechRecognizer.recognitionTask(with: recognitionRequest) { [weak self] (result, error) in
            guard let `self` = self else { return }
            
            var isFinal = false
            if let result = result {
//                print(result.bestTranscription.formattedString)
                isFinal = result.isFinal
                let text = result.bestTranscription.formattedString
                if result.bestTranscription.segments[0].confidence != 0 || isFinal {
                    isFinal = true
                    self.addText("utterance:" + text)
                    self.cotobaCall(url: self.endpointURL,apiKey: self.apiKey,
                                    utterance: text)
                }
            }

            if error != nil || isFinal {
                self.audioEngine.stop()
                self.audioEngine.inputNode.removeTap(onBus: 0)
                self.recognitionTask?.cancel()
                self.recognitionRequest?.endAudio()
                self.recognitionRequest = nil
                self.recognitionTask = nil
            }
        }
        
        let recordingFormat = audioEngine.inputNode.outputFormat(forBus: 0)
        audioEngine.inputNode.installTap(onBus: 0, bufferSize: 1024, format: recordingFormat) { (buffer: AVAudioPCMBuffer, when: AVAudioTime) in
            self.recognitionRequest?.append(buffer)
        }
        
        audioEngine.prepare()
        try? audioEngine.start()
    }
    
    private func sttStop() {
        audioEngine.stop()
        recognitionTask?.cancel()
        recognitionRequest?.endAudio()
    }
}

