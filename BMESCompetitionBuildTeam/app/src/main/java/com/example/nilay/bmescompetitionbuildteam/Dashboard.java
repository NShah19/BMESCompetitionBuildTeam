package com.example.nilay.bmescompetitionbuildteam;

import android.Manifest;
import android.bluetooth.BluetoothAdapter;
import android.bluetooth.BluetoothDevice;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.os.Bundle;
import android.os.Handler;
import android.os.HandlerThread;
import android.support.v4.app.ActivityCompat;
import android.support.v4.content.ContextCompat;
import android.support.v7.app.AppCompatActivity;
import android.text.TextUtils;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;
import android.widget.Toast;

public class Dashboard extends AppCompatActivity {

    private static final int SCAN_PERIOD = 5000;
    private boolean scanning = false;
    private TextView mainText;
    private Handler handler;
    private BluetoothAdapter bluetoothAdapter;
    private BLECustomService bleCustomService;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_dashboard);

        mainText = findViewById(R.id.main_text);

        HandlerThread handlerThread = new HandlerThread("ble");
        handlerThread.start();
        handler = new Handler(handlerThread.getLooper());

        if (ContextCompat.checkSelfPermission(this,
                Manifest.permission.ACCESS_FINE_LOCATION)
                != PackageManager.PERMISSION_GRANTED) {

            // Permission is not granted
            // Should we show an explanation?
            if (ActivityCompat.shouldShowRequestPermissionRationale(this,
                    Manifest.permission.ACCESS_FINE_LOCATION)) {

                // Show an explanation to the user *asynchronously* -- don't block
                // this thread waiting for the user's response! After the user
                // sees the explanation, try again to request the permission.

            } else {

                // No explanation needed; request the permission
                ActivityCompat.requestPermissions(this,
                        new String[]{Manifest.permission.ACCESS_FINE_LOCATION},
                        1234);

                // MY_PERMISSIONS_REQUEST_READ_CONTACTS is an
                // app-defined int constant. The callback method gets the
                // result of the request.
            }
        } else {
            // Permission has already been granted
        }

        Button startScanButton = findViewById(R.id.start_scan_button);
        startScanButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                scanLeDevice(true);
            }
        });

        // Determine if Android device supports Bluetooth
        bluetoothAdapter = BluetoothAdapter.getDefaultAdapter();
        if (bluetoothAdapter == null) {
            Toast.makeText(getApplicationContext(),"Device doesn't Support Bluetooth", Toast.LENGTH_SHORT).show();
            finish();
        // Device does not support Bluetooth
        }

        // Turn on Bluetooth if disabled
        if (!bluetoothAdapter.isEnabled()) {
            Intent enableBtIntent = new Intent(BluetoothAdapter.ACTION_REQUEST_ENABLE);
            startActivityForResult(enableBtIntent, 1);
        }

        bleCustomService = new BLECustomService(this);
    }

    private void scanLeDevice(final boolean enable) {
        if (enable) {
            // Stops scanning after a pre-defined scan period.
            handler.postDelayed(new Runnable() {
                @Override
                public void run() {
                    scanning = false;
                    bluetoothAdapter.stopLeScan(mLeScanCallback);
                    invalidateOptionsMenu();
                }
            }, SCAN_PERIOD);

            scanning = true;
            bluetoothAdapter.startLeScan(mLeScanCallback);
        } else {
            scanning = false;
            bluetoothAdapter.stopLeScan(mLeScanCallback);
        }
        invalidateOptionsMenu();
    }

    private boolean connected;

    // Device scan callback.
    private BluetoothAdapter.LeScanCallback mLeScanCallback =
            new BluetoothAdapter.LeScanCallback() {

                @Override
                public void onLeScan(final BluetoothDevice device, int rssi, byte[] scanRecord) {
                    runOnUiThread(new Runnable() {
                        @Override
                        public void run() {
                            if (!TextUtils.isEmpty(device.getName()) && device.getName().equals("Adafruit Bluefruit LE EA38"))
                                Log.e("Dashboard", "found: " + device.getAddress() + " " + device.getName());
                                bluetoothAdapter.stopLeScan(mLeScanCallback);
                                if (!connected) {
                                    handler.post(new Runnable() {
                                        @Override
                                        public void run() {
                                            bleCustomService.connect(device.getAddress());
                                        }
                                    });
                                }
                                connected = true;
                        }
                    });
                }
            };

    @Override
    protected void onActivityResult(int requestCode, int resultCode, Intent data) {
        Log.v("Dashboard", "got activity result: " + resultCode);

    }

    @Override
    protected void onDestroy() {
        super.onDestroy();
        bleCustomService.disconnect();
        bleCustomService.close();
    }
}
