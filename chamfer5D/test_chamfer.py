import torch
import dist_chamfer_5D as ext
distChamfer = ext.chamfer_5DDist()
import chamfer_python

from torch.autograd import Variable
import time


def test_chamfer():
    distChamfer = ext.chamfer_5DDist()
    p1 = torch.rand(4, 100, 5).cuda()
    p2 = torch.rand(4, 200, 5).cuda()
    points1 = Variable(p1, requires_grad=True)
    points2 = Variable(p2)
    dist1, dist2, idx1, idx2= distChamfer(points1, points2)

    loss = torch.sum(dist1)
    loss.backward()

    mydist1, mydist2, myidx1, myidx2 = chamfer_python.distChamfer(points1, points2)
    d1 = (dist1 - mydist1) ** 2
    d2 = (dist2 - mydist2) ** 2
    assert (
        torch.sum(d1) + torch.sum(d2) < 0.00000001
    ), "chamfer cuda and chamfer normal are not giving the same results"

    xd1 = idx1 - myidx1
    xd2 = idx2 - myidx2
    assert (
            torch.norm(xd1.float()) + torch.norm(xd2.float()) == 0
    ), "chamfer cuda and chamfer normal are not giving the same results"
    print("Unit test passed")


def test_high_dims():
    distChamfer = ext.chamfer_5DDist()
    p1 = torch.rand(4, 100, 5).cuda()
    p2 = torch.rand(4, 200, 5).cuda()
    points1 = Variable(p1, requires_grad=True)
    points2 = Variable(p2)

    mydist1, mydist2, idx1, idx2 = chamfer_python.distChamfer(points1, points2)

    print(mydist1, mydist2, idx1, idx2)

def timings():
    distChamfer = ext.chamfer_5DDist()
    p1 = torch.rand(32, 2000, 5).cuda()
    p2 = torch.rand(32, 1000, 5).cuda()
    print("Timings : Start CUDA version")
    start = time.time()
    for i in range(100):
        points1 = Variable(p1, requires_grad=True)
        points2 = Variable(p2)
        mydist1, mydist2, idx1, idx2 = distChamfer(points1, points2)
        loss = torch.sum(mydist1)
        loss.backward()
    print(f"Ellapsed time is {time.time() - start} seconds.")


    print("Timings : Start Pythonic version")
    start = time.time()
    for i in range(100):
        points1 = Variable(p1, requires_grad=True)
        points2 = Variable(p2)
        mydist1, mydist2, idx1, idx2 = chamfer_python.distChamfer(points1, points2)
        loss = torch.sum(mydist1)
        loss.backward()
    print(f"Ellapsed time is {time.time() - start} seconds.")

test_chamfer()
timings()
# test_high_dims()