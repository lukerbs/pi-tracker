Blockly.Blocks['home'] = {
  init: function() {
    this.appendDummyInput()
        .appendField("Home");
    this.setInputsInline(true);
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour(135);
 this.setTooltip("");
 this.setHelpUrl("");
  }
};

Blockly.Blocks['move_to'] = {
  init: function() {
    this.appendValueInput("j1")
        .setCheck("Number")
        .appendField("Move To:  ")
        .appendField("j1");
    this.appendValueInput("j2")
        .setCheck("Number")
        .appendField("j2");
    this.appendValueInput("j3")
        .setCheck("Number")
        .appendField("j3");
    this.setInputsInline(true);
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour(230);
 this.setTooltip("");
 this.setHelpUrl("");
  }
};

Blockly.Blocks['gripper'] = {
init: function() {
    this.appendDummyInput()
        .appendField("Gripper")
        .appendField(new Blockly.FieldDropdown([["open","OPEN"], ["close","CLOSE"], ["off","OFF"]]), "NAME");
    this.setInputsInline(true);
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour(290);
this.setTooltip("");
this.setHelpUrl("");
}
};


Blockly.Blocks['pause'] = {
  init: function() {
    this.appendValueInput("pause")
        .setCheck("Number")
        .appendField(new Blockly.FieldLabelSerializable("pause (seconds)"), "time");
    this.setInputsInline(true);
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour(0);
 this.setTooltip("");
 this.setHelpUrl("");
  }
};