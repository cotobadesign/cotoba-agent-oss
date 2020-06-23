package com.cotobadesign.agentclient;

import android.graphics.drawable.Drawable;

public class Comment {

    public int userId; // User ID
    public Drawable userIcon; // User icon
    public String text; // utterance

    public Comment(int userId, Drawable userIcon, String text) {
        this.userId = userId;
        this.userIcon = userIcon;
        this.text = text;
    }
}