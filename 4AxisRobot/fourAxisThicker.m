% Home position
theta1 = 0;
theta2 = 0;
theta3 = 0;
theta4 = pi/2;
%theta5=0;
% working good
 DHparameters = [
     0   0  140    theta1;
     0  pi/2    25     theta2;
     250   0   0     theta3;
     0  pi/2   150     theta4;
 
 ];
% DHparameters = [
%     0   0  50    theta1;
%     0  pi/2    25     theta2;
%     250   0   0     theta3;
%     150   -pi/2   0     theta4;
% 
% ];
% Create a robot model                                                      
Robot = rigidBodyTree("DataFormat", "row", "MaxNumBodies", 4);

% Add each body and joint based on DH
% Base joint
Base = rigidBody('Base');
joint1 = rigidBodyJoint('joint1', 'revolute');
setFixedTransform(joint1, DHparameters(1,:), "dh");
Base.Joint = joint1;

% Add a thicker visual (cylinder) for the base
addVisual(Base, "Cylinder", [10 25]); % [Radius, Length]
addBody(Robot, Base, 'base');

% Shoulder joint
Shoulder = rigidBody('Shoulder');
joint2 = rigidBodyJoint('joint2', 'revolute');
setFixedTransform(joint2, DHparameters(2,:), "dh");
Shoulder.Joint = joint2;

% Add a thicker visual (cylinder) for the shoulder
addVisual(Shoulder, "Cylinder", [10 250]); % [Radius, Length]
addBody(Robot, Shoulder, 'Base');

% Elbow joint
Elbow = rigidBody('Elbow');
joint3 = rigidBodyJoint('joint3', 'revolute');
setFixedTransform(joint3, DHparameters(3,:), "dh");
Elbow.Joint = joint3;

% Add a thicker visual (cylinder) for the elbow
addVisual(Elbow, "Cylinder", [10 150]); % [Radius, Length]
addBody(Robot, Elbow, 'Shoulder');

% Wrist joint
Wrist = rigidBody('Wrist');
joint4 = rigidBodyJoint('joint4', 'revolute');
setFixedTransform(joint4, DHparameters(4,:), 'dh');
Wrist.Joint = joint4;

addVisual(Wrist, "Cylinder", [10 50]); % [Radius, Length]
addBody(Robot, Wrist, 'Elbow');

figure;
show(Robot);
title("4XflexARM - Thicker Links");

