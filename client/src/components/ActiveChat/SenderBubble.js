import React, { useEffect, useState } from 'react';
import { makeStyles } from '@material-ui/core/styles';
import { Avatar, Box, Typography } from '@material-ui/core';

const useStyles = makeStyles(() => ({
  root: {
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'flex-end',
  },
  date: {
    fontSize: 11,
    color: '#BECCE2',
    fontWeight: 'bold',
    marginBottom: 5,
  },
  readAvatar: {
    height: 20,
    width: 20,
    borderRadius: '50%',
    backgroundColor: '#bbb'
  },
  text: {
    fontSize: 14,
    color: '#91A3C0',
    letterSpacing: -0.2,
    padding: 8,
    fontWeight: 'bold',
  },
  bubble: {
    background: '#F4F6FA',
    borderRadius: '10px 10px 0 10px',
  },
}));

const SenderBubble = ({ time, text, readPhotoUrl }) => {
  const classes = useStyles();
  const [showPhotoUrl, setShowPhotoUrl] = useState(false);
  
  useEffect(() => {
    setShowPhotoUrl(readPhotoUrl !== undefined)
  }, [readPhotoUrl])

  return (
    <Box className={classes.root}>
      <Typography className={classes.date}>{time}</Typography>
      <Box className={classes.bubble}>
        <Typography className={classes.text}>{text}</Typography>
      </Box>
      {showPhotoUrl && 
        <Avatar src={readPhotoUrl} className={classes.readAvatar}/>
      }
    </Box>
  );
};

export default SenderBubble;
