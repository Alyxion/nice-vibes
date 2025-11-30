# Sample Applications

Working example applications demonstrating NiceGUI patterns.

## Gallery

<!-- GALLERY_START -->
<table>
<tr>
<td align="center" valign="top" width="33%">
<div style="height: 40px; display: flex; align-items: center; justify-content: center;">
<a href="bouncing_circle/"><strong>Bouncing Circle Animation</strong></a>
</div>
<a href="bouncing_circle/"><img src="bouncing_circle/animated.gif" width="280"></a><br>
<sub>A sample demonstrating custom JavaScript/Vue components with Python-side rendering using PIL.</sub>
</td>
<td align="center" valign="top" width="33%">
<div style="height: 40px; display: flex; align-items: center; justify-content: center;">
<a href="dashboard/"><strong>Analytics Dashboard</strong></a>
</div>
<a href="dashboard/"><img src="dashboard/screenshot.jpg" width="280"></a><br>
<sub>A comprehensive analytics dashboard showcasing NiceGUI's charting and input control capabilities with an object-oriented architecture.</sub>
</td>
<td align="center" valign="top" width="33%">
<div style="height: 40px; display: flex; align-items: center; justify-content: center;">
<a href="multi_dashboard/"><strong>Multi-Dashboard Application</strong></a>
</div>
<a href="multi_dashboard/"><img src="multi_dashboard/screenshot.jpg" width="280"></a><br>
<sub>A full SPA demonstrating authentication, signed cookie persistence, role-based permissions, and auto-discovered pages.</sub>
</td>
</tr>
<tr>
<td align="center" valign="top" width="33%">
<div style="height: 40px; display: flex; align-items: center; justify-content: center;">
<a href="stock_peers/"><strong>Stock Peer Analysis Dashboard</strong></a>
</div>
<a href="stock_peers/"><img src="stock_peers/screenshot.jpg" width="280"></a><br>
<sub>Compare multiple stocks against their peer group average.</sub>
</td>
<td align="center" valign="top" width="33%">
<div style="height: 40px; display: flex; align-items: center; justify-content: center;">
<a href="sub_pages_demo/"><strong>Sub Pages Demo - Multi-App Navigation</strong></a>
</div>
<a href="sub_pages_demo/"><img src="sub_pages_demo/screenshot.jpg" width="280"></a><br>
<sub>A demonstration of NiceGUI's `ui.sub_pages` for building Single Page Applications (SPAs) with persistent client state.</sub>
</td>
<td align="center" valign="top" width="33%">
<div style="height: 40px; display: flex; align-items: center; justify-content: center;">
<a href="threejs_tornado/"><strong>Three.js Tornado Visualization</strong></a>
</div>
<a href="threejs_tornado/"><img src="threejs_tornado/animated.gif" width="280"></a><br>
<sub>A stunning 3D tornado particle system demonstrating advanced Three.js integration with NiceGUI.</sub>
</td>
</tr>
</table><!-- GALLERY_END -->

## Running a Sample

```bash
cd samples/<sample_name>
poetry run python main.py
```

Then open http://localhost:8080
