import React, {useState} from "react";
import { Box, Typography } from "@material-ui/core";
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
  unreadCount: {
    backgroundColor: "#3A8DFF",
    fontSize: 14,
    fontWeight: "bold",
    textAlign: "center",
    color: "#FFFFFF",
    borderRadius: '15px',
    padding: "2px 8px 2px 8px",
    marginRight: 10,
  }
}));

const ChatContent = ({ conversation }) => {
  const classes = useStyles();
  const [unreadCount, setUnreadCount] = useState(conversation.unreadCount);

  const { otherUser } = conversation;
  const latestMessageText = conversation.id && conversation.latestMessageText;

  return (
    <Box className={classes.root} onClick={() => setUnreadCount(0)}>
      <Box>
        <Typography className={classes.username}>
          {otherUser.username}
        </Typography>
        <Typography className={classes.previewText}>
          {latestMessageText}
        </Typography>
      </Box>
      {unreadCount > 0 ? (
        <Box>
          <Typography className={classes.unreadCount}>
            {unreadCount}
          </Typography>
        </Box>
      ) : null}
    </Box>
  );
};

export default ChatContent;
