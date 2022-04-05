import React, { useEffect, useRef, useState } from "react";
import axios from "axios";
import { Box, Typography, Badge } from "@material-ui/core";
import { makeStyles } from "@material-ui/core/styles";

const useStyles = makeStyles((theme) => ({
  root: {
    display: "flex",
    justifyContent: "space-between",
    marginLeft: 20,
    flexGrow: 1,
  },
  username: {
    fontWeight: "bold",
    letterSpacing: -0.2,
  },
  previewText: {
    fontSize: 12,
    color: "#9CADC8",
    letterSpacing: -0.17,
  },
  boldPreview: {
    fontWeight: "bold",
  },
  unreadCount: {
    display: "inline-block",
    width: "30px",
    height: "30px",
    lineHeight: "30px",
    borderRadius: '15px',
    marginRight: 10,
    backgroundColor: "#3A8DFF",
    fontSize: 14,
    fontWeight: "bold",
    textAlign: "center",
    color: "#FFFFFF",
  }
}));


const ChatContent = ({ conversation }) => {
  const classes = useStyles();
  const [unreadCount, setUnreadCount] = useState(conversation.unreadCount);
  const showUnreadAttributes = useRef(unreadCount > 0);
  
  const { otherUser } = conversation;
  const latestMessageText = conversation.id && conversation.latestMessageText;
  
  const updateRead = async (conversation) => {
    if (conversation && conversation.messages.length > 0) {
      try {
        await axios.patch("/api/conversations/readreceipt", {conversationId : conversation.id});
      } catch (error) {
        console.error(error);
      }
    }
  };

  useEffect(() => {
    setUnreadCount(conversation.unreadCount);
    showUnreadAttributes.current = conversation.unreadCount > 0;
  }, [conversation])
  
  return (
    <Box className={classes.root} onClick={() => updateRead(conversation)}>
      <Box>
        <Typography className={classes.username}>
          {otherUser.username}
        </Typography>
        <Typography className={[classes.previewText, showUnreadAttributes.current && classes.boldPreview].join(' ')}>
          {latestMessageText}
        </Typography>
      </Box>
      {showUnreadAttributes.current && 
        <Badge className={classes.unreadCount}>
          {unreadCount}
        </Badge>
      }
    </Box>
  );
};

export default ChatContent;
