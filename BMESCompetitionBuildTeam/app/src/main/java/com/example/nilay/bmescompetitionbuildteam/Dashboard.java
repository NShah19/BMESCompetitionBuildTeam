package com.example.nilay.bmescompetitionbuildteam;

import android.bluetooth.BluetoothAdapter;
import android.bluetooth.BluetoothDevice;
import android.bluetooth.BluetoothSocket;
import android.content.Intent;
import android.os.Handler;
import android.os.Message;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.widget.Toast;

import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.util.Iterator;
import java.util.Set;
import java.util.UUID;

public class Dashboard extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_dashboard);

        // Determine if Android device supports Bluetooth
        final BluetoothAdapter mBluetoothAdapter = BluetoothAdapter.getDefaultAdapter();
        if (mBluetoothAdapter == null) {
            Toast.makeText(getApplicationContext(),"Device doesn't Support Bluetooth", Toast.LENGTH_SHORT).show();
        // Device does not support Bluetooth
        }

        // Turn on Bluetooth if disabled
        if (!mBluetoothAdapter.isEnabled()) {
            Intent enableBtIntent = new Intent(BluetoothAdapter.ACTION_REQUEST_ENABLE);
            startActivityForResult(enableBtIntent, 1);
        }

        Toast.makeText(Dashboard.this,"ACP Pradyuman is the BEAST", Toast.LENGTH_SHORT).show();


        // Thread used for transferring data
        class ConnectedThread extends Thread {
            private final BluetoothSocket mmSocket;
            private final InputStream mmInStream;
            private final OutputStream mmOutStream;
            public ConnectedThread(BluetoothSocket socket) {
                Toast.makeText(Dashboard.this,"Test 6", Toast.LENGTH_SHORT).show();
                mmSocket = socket;
                InputStream tmpIn = null;
                OutputStream tmpOut = null;
                try {
                    tmpIn = socket.getInputStream();
                    tmpOut = socket.getOutputStream();
                } catch (IOException e) { }
                mmInStream = tmpIn;
                mmOutStream = tmpOut;
            }
            public void run() {
                Toast.makeText(Dashboard.this,"Test 7", Toast.LENGTH_SHORT).show();
                byte[] buffer = new byte[1024];
                int begin = 0;
                int bytes = 0;
                while (true) {
                    try {
                        bytes += mmInStream.read(buffer, bytes, buffer.length - bytes);
                        for(int i = begin; i < bytes; i++) {
                            if(buffer[i] == "#".getBytes()[0]) {
                                Handler mHandler = null;
                                mHandler.obtainMessage(1, begin, i, buffer).sendToTarget();
                                begin = i + 1;
                                if(i == bytes - 1) {
                                    bytes = 0;
                                    begin = 0;
                                }
                            }
                        }
                    } catch (IOException e) {
                        break;
                    }
                }
            }
            public void write(byte[] bytes) {
                try {
                    mmOutStream.write(bytes);
                } catch (IOException e) { }
            }
            public void cancel() {
                try {
                    mmSocket.close();
                } catch (IOException e) { }
            }
        }

        // Thread used for connecting Bluetooth devices
        class ConnectThread extends Thread {
            private final BluetoothSocket mmSocket;
            private final BluetoothDevice mmDevice;
            private final UUID MY_UUID = UUID.fromString("00001101-0000-1000-8000-00805F9B34FB");
            public ConnectThread(BluetoothDevice device) {
                Toast.makeText(Dashboard.this,"Test 3", Toast.LENGTH_SHORT).show();

                BluetoothSocket tmp = null;
                mmDevice = device;
                try {
                    tmp = device.createRfcommSocketToServiceRecord(MY_UUID);
                } catch (IOException e) { }
                mmSocket = tmp;
                Toast.makeText(Dashboard.this,"Test 4", Toast.LENGTH_SHORT).show();

            }
            public void run() {
                Toast.makeText(Dashboard.this,"Test 5", Toast.LENGTH_SHORT).show();
                mBluetoothAdapter.cancelDiscovery();
                try {
                    mmSocket.connect();
                } catch (IOException connectException) {
                    try {
                        mmSocket.close();
                    } catch (IOException closeException) {
                    }
                    Toast.makeText(Dashboard.this,"KILL ME NOW", Toast.LENGTH_SHORT).show();
                    return;
                }

                Toast.makeText(Dashboard.this,"Work", Toast.LENGTH_SHORT).show();

                ConnectedThread mConnectedThread = new ConnectedThread(mmSocket);
                mConnectedThread.run();

                Toast.makeText(Dashboard.this,"Please work", Toast.LENGTH_SHORT).show();


            }
            public void cancel() {
                try {
                    mmSocket.close();
                } catch (IOException e) {
                }
            }
        }

        // Create the connection thread
        // Get the Bluetooth module device
        BluetoothDevice mDevice = null;
        Set<BluetoothDevice> pairedDevices = mBluetoothAdapter.getBondedDevices();
        if (pairedDevices.size() > 0) {
            for (BluetoothDevice device : pairedDevices) {
                String deviceName = device.getName();
                String deviceHardwareAddress = device.getAddress();
                Toast.makeText(Dashboard.this,deviceName, Toast.LENGTH_SHORT).show();
                if(deviceName.equals("Adafruit Bluefruit LE")) {
                    mDevice = device;
                    break;
                }
            }
        }
        Toast.makeText(Dashboard.this,"Test 1", Toast.LENGTH_SHORT).show();

        ConnectThread mConnectThread = new ConnectThread(mDevice);
        mConnectThread.run();

        Toast.makeText(Dashboard.this,"Test 2", Toast.LENGTH_SHORT).show();



        // Handler code
        Handler mHandler = new Handler() {
            @Override
            public void handleMessage(Message msg) {
                Toast.makeText(Dashboard.this,"Test 8", Toast.LENGTH_SHORT).show();
                byte[] writeBuf = (byte[]) msg.obj;
                int begin = msg.arg1;
                int end = (int)msg.arg2;

                switch(msg.what) {
                    case 1:
                        String writeMessage = new String(writeBuf);
                        writeMessage = writeMessage.substring(begin, end);
                        Toast.makeText(Dashboard.this, writeMessage, Toast.LENGTH_SHORT).show();
                        break;
                }
                        }
                        };
    }
}
