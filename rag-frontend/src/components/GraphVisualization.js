import React, { useEffect, useRef } from 'react'
import ForceGraph2D from 'react-force-graph-2d'

function GraphVisualization ({ graphData }) {
  const graphRef = useRef()

  useEffect(() => {
    if (graphRef.current) {
      graphRef.current.d3Force('link').distance(100)
      graphRef.current.d3Force('charge').strength(-100)
    }
  }, [])

  if (!graphData || !graphData.nodes.length) {
    return null
  }

  return (
    <div className='border rounded bg-white p-2' style={{ height: '300px' }}>
      <ForceGraph2D
        ref={graphRef}
        graphData={graphData}
        nodeLabel='label'
        linkLabel='label'
        nodeColor='#2563eb'
        linkColor='#94a3b8'
        nodeRelSize={6}
        linkDirectionalArrowLength={6}
        linkDirectionalArrowRelPos={0.8}
      />
    </div>
  )
}

export default GraphVisualization
