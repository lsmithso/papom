# papom - Pulseaudio  Python Object Model

## Introduction

Pulseaudio is plumbing for audio in Linux. It allows clients
(applications) and audio Sources and Sinks to be plugged together and
moved around at run time.  Unfortunately there   is no simple way to control Pulseaudio from Python.  papom attempts to solve this. 

papom uses the Pulseaudio d-bus interface to build an object model of
the current client/source/sink connections.  It connects objects
together to represent the connections between the clients and
source/sinks, and adds operations to display, configure and move
connections between the nodes.

A key feature of papom is that Sinks/Sources may be identified by
their human readable name, and not just by an index number as provided
by pactl or pacmd. Furthermore clients may be selected by the pid or
process name.

## Usage

The main use of papam is as a Python module to be used by applications
wishing to control Pulseaudio. Included with papom is a CLI program that emulates some of the functions of pactl and pacmd, although this is not its main purpose. 

```
Example code here
```


## Install

Need Pulseaudio dbus module installed. 

easy_install

github

## papomc command line program

## papom classes

## Licence


