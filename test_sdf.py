import sdformat14 as sdf
import sys

sdf_str = """<?xml version="1.0" ?>
<sdf version="1.9">
  <model name="test">
    <link name="link">
      <sensor name="lidar" type="ray">
        <ray><scan><horizontal><samples>1</samples><resolution>1</resolution></horizontal></scan><range><min>0</min><max>1</max></range></ray>
      </sensor>
    </link>
  </model>
</sdf>
"""

root = sdf.Root()
root.load_sdf_string(sdf_str)
sensor = root.model().link_by_index(0).sensor_by_index(0)
print(f"Sensor type: {sensor.type()}")
print(f"LIDAR: {sdf.Sensortype.LIDAR}")
print(f"RAY: {getattr(sdf.Sensortype, 'RAY', 'NOT_FOUND')}")
print(f"GPU_RAY: {getattr(sdf.Sensortype, 'GPU_RAY', 'NOT_FOUND')}")
