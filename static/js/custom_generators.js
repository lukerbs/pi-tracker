Blockly.Python['move_to'] = function(block) {
  var value_j1 = Blockly.Python.valueToCode(block, 'j1', Blockly.Python.ORDER_ATOMIC);
  var value_j2 = Blockly.Python.valueToCode(block, 'j2', Blockly.Python.ORDER_ATOMIC);
  var value_j3 = Blockly.Python.valueToCode(block, 'j3', Blockly.Python.ORDER_ATOMIC);
  var code = 'device.rotate_joint('+ value_j1 +', '+ value_j2 +', '+ value_j3 +', 0.779, wait=True)\n\n';
  return code;
};

  Blockly.Python['gripper'] = function(block) {
    var dropdown_name = block.getFieldValue('NAME');
    if (dropdown_name == 'OPEN') {
        var code = 'device.grip(False)\n\n';
    } else if (dropdown_name == 'CLOSE') {
        var code = 'device.grip(True)\n\n';
    } else {
        var code = 'device.suck(False)\n\n';
    }
    return code;
  };

  Blockly.Python['home'] = function(block) {
    var code = 'device.rotate_joint(0, 0, 0, 0.779, wait=True)\n';
    return code;
  };


  Blockly.Python['pause'] = function(block) {
    var value_pause = Blockly.Python.valueToCode(block, 'pause', Blockly.Python.ORDER_ATOMIC);
    var code = 'time.sleep(' + String(value_pause) + ')\n';
    return code;
  };