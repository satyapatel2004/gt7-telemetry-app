import React, { useEffect, useState } from 'react';
import io from 'socket.io-client';
import { Box, Container, Grid, CssBaseline, Typography } from '@mui/material';
import LapTimes from './LapTimes';
import LEDBar from './LEDBar';
import LapVis from './LapVis';
import { createTheme, ThemeProvider } from '@mui/material/styles';
import '@fontsource/roboto-mono'; 

// Create theme with Roboto Mono font
const theme = createTheme({
  typography: {
    fontFamily: 'Roboto Mono, monospace',
  },
});

// Connect to the Flask server
const socket = io('http://127.0.0.1:5000');

function App() {
  const [throttle, setThrottle] = useState(0);
  const [lapData, setLapData] = useState([]);

  useEffect(() => {
    socket.on('throttle_data', (data) => {
      setThrottle(data.throttle);
    });

    socket.on('lap_data', (data) => {
      setLapData((prevLapData) => [...prevLapData, data]);
    });

    return () => {
      socket.off('throttle_data');
      socket.off('lap_data');
    };
  }, []);

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Container
        sx={{
          backgroundColor: '#2b2b2b',
          color: '#fff',
          padding: '20px',
          minHeight: '100vh',
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'flex-start',
          width: '100vw',
          margin: 0,
          maxWidth: 'none',
          borderRadius: '0px',
        }}
      >
        {/* Logo centered at the top */}
        <Box
          component="img"
          src={`${process.env.PUBLIC_URL}/GTLogo.png`}  // Path to logo
          alt="GT Logo"
          sx={{
            width: '300px',  // Increase logo size
            marginBottom: '40px',  // Space between logo and other content
          }}
        />
        
        {/* Other content below the logo */}
        <Grid container spacing={3} justifyContent="center">
          {/* Throttle Indicator with Label */}
          <Grid item xs={12} md={6}>
            <Typography variant="h6" sx={{ marginBottom: '10px', color: '#fff', textAlign: 'center' }}>
              Throttle
            </Typography>
            <LEDBar throttle={throttle} />
          </Grid>

          {/* Lap Times */}
          <Grid item xs={12} md={6}>
            <LapTimes lapData={lapData} />
          </Grid>

          {/* Lap Visualizations */}
          <Grid item xs={12}>
            <Grid container spacing={2} justifyContent="center">
              {lapData.map((lap, index) => (
                <Grid item xs={12} md={4} key={index}>
                  <LapVis lap={lap} />
                </Grid>
              ))}
            </Grid>
          </Grid>
        </Grid>
      </Container>
    </ThemeProvider>
  );
}

export default App;
