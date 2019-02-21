import unittest
import pcl
import numpy as np


class loader_visualizer(unittest.TestCase):
    def test_add_callback(self, cloud, labelfile, database_name):
        def key_callback(event):
            print(event.KeyCode, event.KeySym)

        def mouse_callback(event):
            print(event.X, event.Y, event.Type, event.Button)

        def picking_callback(event):
            print(event.Point, event.PointIndex)

        def area_callback(event):
            print(event.PointsIndices)

        def bounding_box_apollo(para_list, line_num, r, b, g):
            center = np.matrix([para_list[0], para_list[1], para_list[2]]).T*np.ones((1,8))
            size = np.matrix([[para_list[3],0,0], [0,para_list[4],0], [0,0,para_list[5]]])
            vertex = center + size*np.matrix([[.5,.5,-.5,-.5,.5,.5,-.5,-.5],[.5,-.5,-.5,.5,.5,-.5,-.5,.5],[.5,.5,.5,.5,-.5,-.5,-.5,-.5]])
            for i in range(3):
                viewer.addLine(vertex[:,i], vertex[:,i+1], r, b, g, id=str(line_num))
                viewer.addLine(vertex[:,i+4], vertex[:,i+5], r, b, g, id=str(4+line_num))
                viewer.addLine(vertex[:,i], vertex[:,i+4], r, b, g, id=str(8+line_num))
                line_num += 1
            viewer.addLine(vertex[:,3], vertex[:,0], r, b, g, id=str(line_num))
            viewer.addLine(vertex[:,4], vertex[:,7], r, b, g, id=str(4 +line_num))
            viewer.addLine(vertex[:,3], vertex[:,7], r, b, g, id=str(8+line_num))

        lines = 0

        viewer = pcl.Visualizer()
        viewer.addPointCloud(cloud)

        viewer.addCoordinateSystem()

        # addLine(self, p1, p2, double r=0.5, double g=0.5, double b=0.5, str id="line", int viewport=0)
        # addText(self, str text, int xpos, int ypos, int fontsize = 10, double r = 1, double g = 1, double b = 1, str id = "", int viewport = 0)
        file = open(labelfile, 'r')
        if database_name == "apollo":
            for obj_line in file:
                obj_line = obj_line.split()
                obj_para = [float(i) for i in obj_line[1:7]]
                if obj_line[0] == "vehicle":  # red
                    r = 1; g = 0; b = 0
                    bounding_box_apollo(obj_para, lines, r, b, g)
                    lines += 12
                elif obj_line[0] == "pedestrian":  # blue
                    r = 0; g = 1; b = 0
                    bounding_box_apollo(obj_para, lines, r, b, g)
                    lines += 12
                elif obj_line[0] == "cyclist":  # green
                    r = 0; g = 0; b = 1
                    bounding_box_apollo(obj_para, lines, r, b, g)
                    lines += 12
                else:  # don't care
                    r = 0.7; g = 0.7; b = 0.1
                    bounding_box_apollo(obj_para, lines, r, b, g)
                    lines += 12
        elif database_name == "kitti":
            pass

        viewer.registerKeyboardCallback(key_callback)
        viewer.registerMouseCallback(mouse_callback)
        viewer.registerPointPickingCallback(picking_callback)
        viewer.registerAreaPickingCallback(area_callback)

        viewer.spinOnce(time=2e9)
        viewer.close()


if __name__ == "__main__":
    dir_apollo = "/media/songanz/New Volume/data/Apollo/3d-sample-lidar/"
    dir_kitti = "/media/songanz/New Volume/data/KITTI/Object/training/"
    dir_night = "/media/songanz/New Volume/data/Night data/12_05/Original_Large_Files/binary/"

    frame = 0

    filename_apollo = dir_apollo + "bin_files/" + "002_%08d" % frame + ".bin"
    labelfile_apollo = dir_apollo + "label_file/" + "002_%08d" % frame + ".bin.txt"

    filename_kitti = dir_kitti + "velodyne/" + "%06d" % frame + ".bin"
    labelfile_kitti = dir_kitti + "label_2/" + "%06d" % frame + ".txt"

    filename_night = dir_night + "%06d" % frame + ".bin"

    cloud_apollo = pcl.load_bin(filename_apollo, "xyzi")
    cloud_kitti = pcl.load_bin(filename_kitti, "xyzi")
    cloud_night = pcl.load_bin(filename_night, 'xyzi')

    visualizer = loader_visualizer()

    # visualizer.test_add_callback(cloud_apollo, labelfile_apollo, "apollo")
    # TODO: visualize kitti
    # visualizer.test_add_callback(cloud_kitti, labelfile_kitti, "kitti")
    visualizer.test_add_callback(cloud_night, labelfile_kitti, "kitti")
