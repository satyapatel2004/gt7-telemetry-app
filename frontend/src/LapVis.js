import { Card, CardContent, Typography } from '@mui/material';
import Plot from 'react-plotly.js';

function LapVisualization({ lap }) {
  return (
    <Card sx={{ backgroundColor: '#222', color: '#fff', padding: '10px', borderRadius: '10px' }}>
      <CardContent>
        <Typography variant="h6" sx={{ textAlign: 'center', color: 'yellow' }}>Lap {lap.lapno} Visualization</Typography>
        {lap.coordinates && lap.coordinates.length > 0 ? (
          <Plot
            data={[
              {
                x: lap.coordinates.map(coord => coord[0]),
                y: lap.coordinates.map(coord => coord[1]),
                z: lap.coordinates.map(coord => coord[2]),
                mode: 'lines',
                line: {
                  width: 4,
                  color: lap.coordinates.map(coord => {
                    const throttleValue = coord[4];
                    const brakingValue = coord[3];
                    if (throttleValue > 0) {
                      const greenIntensity = Math.min(255, Math.floor((throttleValue / 100) * 255));
                      return `rgb(${255 - greenIntensity}, ${greenIntensity}, 0)`;  // Red to green
                    } else if (brakingValue > 0) {
                      const redIntensity = Math.min(255, Math.floor((brakingValue / 100) * 255));
                      return `rgb(${redIntensity}, 0, 0)`;  // Darker red as braking increases
                    }
                    return 'rgb(128,128,128)';  // Neutral color if neither throttle nor braking
                  }),
                },
                type: 'scatter3d',
              }
            ]}
            layout={{
              autosize: true,
              scene: {
                xaxis: { showgrid: false, zeroline: false, showticklabels: false },
                yaxis: { showgrid: false, zeroline: false, showticklabels: false },
                zaxis: { showgrid: false, zeroline: false, showticklabels: false },
                aspectratio: { x: 1, y: 1, z: 0.5 },
              },
              margin: { l: 0, r: 0, b: 0, t: 0 },
              height: 200,
            }}
            style={{ width: '100%', height: '200px' }}
          />
        ) : (
          <Typography variant="body2" sx={{ textAlign: 'center', color: 'red' }}>
            No coordinates available.
          </Typography>
        )}
      </CardContent>
    </Card>
  );
}

export default LapVisualization;