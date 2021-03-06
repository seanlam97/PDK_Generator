from . import *

class Contra_DC_custom(pya.PCellDeclarationHelper):
  """
  Author:   Mustafa Hammood 
                Mustafa@ece.ubc.ca
  """

  def __init__(self):

    # Important: initialize the super class
    super(Contra_DC_custom, self).__init__()
    TECHNOLOGY = get_technology_by_name('{orig-techname}')

    # declare the parameters
    self.param("number_of_periods1", self.TypeInt, "Number of grating periods", default = {n-periods})
    self.param("grating_period1", self.TypeDouble, "Grating period (inner)", default = {grating-period1})
    self.param("grating_period2", self.TypeDouble, "Grating period (outer)", default = {grating-period2})
    self.param("gap", self.TypeDouble, "Gap (microns)", default = {gap})
    self.param("corrugation_width1outer", self.TypeDouble, "Waveguide 1 Corrugration width (outer)", default = {corrugation-width1-outer})
    self.param("corrugation_width1inner", self.TypeDouble, "Waveguide 1 Corrugration width (inner)", default = {corrugation-width1-inner})
    self.param("corrugation_width2outer", self.TypeDouble, "Waveguide 2 Corrugration width (inner)", default = {corrugation-width2-outer})
    self.param("corrugation_width2inner", self.TypeDouble, "Waveguide 2 Corrugration width (outer)", default = {corrugation-width2-inner})
    self.param("wg1_width", self.TypeDouble, "Waveguide 1 width", default = {waveguide1-width})
    self.param("wg2_width", self.TypeDouble, "Waveguide 2 width", default = {waveguide2-width})
    self.param("index", self.TypeDouble, "Gaussian Index", default = {gaussian-index})
    
    # declare layer params
    self.param("layer", self.TypeLayer, "Layer", default = TECHNOLOGY['{{Layer}Waveguide}'], hidden = True)
    self.param("pinrec", self.TypeLayer, "PinRec Layer", default = TECHNOLOGY['{{Layer}PinRec}'], hidden = True)
    self.param("devrec", self.TypeLayer, "DevRec Layer", default = TECHNOLOGY['{{Layer}DevRec}'], hidden = True)
    self.param("textl", self.TypeLayer, "Text Layer", default = TECHNOLOGY['{{Layer}Text}'], hidden = True)

  def display_text_impl(self):
    # Provide a descriptive text for the cell
    return "Contra_DC_custom%s-%.3f" % \
    (self.number_of_periods1, self.grating_period1)
  
  def coerce_parameters_impl(self):
    pass

  def can_create_from_shape(self, layout, shape, layer):
    return False
    
  def produce_impl(self):
  
    # fetch the parameters
    dbu = self.layout.dbu
    ly = self.layout
    shapes = self.cell.shapes

    LayerSi = self.layer
    LayerSiN = ly.layer(LayerSi)
    LayerPinRecN = ly.layer(self.pinrec)
    LayerDevRecN = ly.layer(self.devrec)

    from SiEPIC.extend import to_itype
    
    # Draw the Bragg grating (bottom):
    width_period1 = to_itype(self.grating_period1/2,dbu)
    width_period2 = to_itype(self.grating_period2/2,dbu)
    
    grating_period1 = to_itype(self.grating_period1,dbu)
    grating_period2 = to_itype(self.grating_period2,dbu)

    w1 = to_itype(self.wg1_width,dbu)
    w2 = to_itype(self.wg2_width,dbu)
    
    GaussianIndex = self.index

    N1 = self.number_of_periods1
    
    vertical_offset1 = to_itype(self.gap/2 + self.wg1_width/2, dbu)
    vertical_offset2 = to_itype(-self.gap/2 - self.wg2_width/2, dbu)
    
    for i in range(0,self.number_of_periods1):
      x1 = to_itype(i * self.grating_period1,dbu)
      x2 = to_itype(i * self.grating_period2,dbu)
      
      profileFunction = math.exp( -0.5*(2*GaussianIndex*(i-N1/2)/(N1))**2 )
      
      profile_outer = to_itype(self.corrugation_width1outer,dbu)*profileFunction
      profile_inner = to_itype(self.corrugation_width1inner,dbu)*profileFunction
      
      box1outer = Box(x1, vertical_offset1+w1/2-profile_outer/2, x1 + width_period1, vertical_offset1)
      box2outer = Box(x1+width_period1, vertical_offset1+w1/2+profile_outer/2, x1 + 2*width_period1, vertical_offset1)
      
      box1inner = Box(x2, vertical_offset1-w1/2-profile_inner/2, x2 + width_period2, vertical_offset1)
      box2inner = Box(x2+width_period2, vertical_offset1-w1/2+profile_inner/2, x2 + 2*width_period2, vertical_offset1)
      
      shapes(LayerSiN).insert(box1outer)
      shapes(LayerSiN).insert(box2outer)

      shapes(LayerSiN).insert(box1inner)
      shapes(LayerSiN).insert(box2inner)
      
      length1 = x1 + grating_period1
      length2 = x2 + grating_period2
    
    if grating_period1 > grating_period2:
      box_inner = Box(length2, vertical_offset1, length1, vertical_offset1-w1/2)
      shapes(LayerSiN).insert(box_inner)
      length = x1 + grating_period1
    else:
      box_outer = Box(length1, vertical_offset1, length2, vertical_offset1+w1/2)
      shapes(LayerSiN).insert(box_outer)
      length = x2 + grating_period2

    # lower waveguide
    for i in range(0,self.number_of_periods1):
      x1 = to_itype(i * self.grating_period1,dbu)
      x2 = to_itype(i * self.grating_period2,dbu)
      
      profileFunction = math.exp( -0.5*(2*GaussianIndex*(i-N1/2)/(N1))**2 )
      
      profile_outer = to_itype(self.corrugation_width2outer,dbu)*profileFunction
      profile_inner = to_itype(self.corrugation_width2inner,dbu)*profileFunction
      
      box1outer = Box(x2, vertical_offset2+w2/2+profile_outer/2, x2 + width_period2, vertical_offset2)
      box2outer = Box(x2+width_period2, vertical_offset2+w2/2-profile_outer/2, x2 + 2*width_period2, vertical_offset2)
      
      box1inner = Box(x1, vertical_offset2-w2/2+profile_inner/2, x1 + width_period1, vertical_offset2)
      box2inner = Box(x1+width_period1, vertical_offset2-w2/2-profile_inner/2, x1 + 2*width_period1, vertical_offset2)
      
      shapes(LayerSiN).insert(box1outer)
      shapes(LayerSiN).insert(box2outer)

      shapes(LayerSiN).insert(box1inner)
      shapes(LayerSiN).insert(box2inner)
      
      length1 = x1 + grating_period1
      length2 = x2 + grating_period2
    
    if grating_period1 > grating_period2:
      box_inner = Box(length2, vertical_offset2, length1, vertical_offset2+w2/2)
      shapes(LayerSiN).insert(box_inner)
      length = x1 + grating_period1
    else:
      box_outer = Box(length1, vertical_offset2, length2, vertical_offset2-w2/2)
      shapes(LayerSiN).insert(box_outer)
      length = x2 + grating_period2

    # Create the pins on the waveguides, as short paths:
    from SiEPIC._globals import PIN_LENGTH as pin_length

    w = to_itype(self.wg2_width,dbu)
    t = Trans(Trans.R0, 0,vertical_offset2)
    pin = Path([Point(pin_length/2, 0), Point(-pin_length/2, 0)], w)
    pin_t = pin.transformed(t)
    shapes(LayerPinRecN).insert(pin_t)
    text = Text ("pin1", t)
    shape = shapes(LayerPinRecN).insert(text)
    shape.text_size = 0.4/dbu
    
    w = to_itype(self.wg1_width,dbu)
    t = Trans(Trans.R0, 0,vertical_offset1)
    pin = Path([Point(pin_length/2, 0), Point(-pin_length/2, 0)], w)
    pin_t = pin.transformed(t)
    shapes(LayerPinRecN).insert(pin_t)
    text = Text ("pin3", t)
    shape = shapes(LayerPinRecN).insert(text)
    shape.text_size = 0.4/dbu

    w = to_itype(self.wg1_width,dbu)
    t = Trans(Trans.R0, length,vertical_offset1)
    pin = Path([Point(-pin_length/2, 0), Point(pin_length/2, 0)], w)
    pin_t = pin.transformed(t)
    shapes(LayerPinRecN).insert(pin_t)
    text = Text ("pin2", t)
    shape = shapes(LayerPinRecN).insert(text)
    shape.text_size = 0.4/dbu
    
    w = to_itype(self.wg2_width,dbu)
    t = Trans(Trans.R0, length,vertical_offset2)
    pin = Path([Point(-pin_length/2, 0), Point(pin_length/2, 0)], w)
    pin_t = pin.transformed(t)
    shapes(LayerPinRecN).insert(pin_t)
    text = Text ("pin4", t)
    shape = shapes(LayerPinRecN).insert(text)
    shape.text_size = 0.4/dbu

    # Compact model information
    t = Trans(Trans.R0, 0, 0)
    text = Text ('Lumerical_INTERCONNECT_library=Design kits/{orig-techname}', t)
    shape = shapes(LayerDevRecN).insert(text)
    shape.text_size = 0.1/dbu
    t = Trans(Trans.R0, length/10, 0)
    text = Text ('Component={cm-name}', t)
    shape = shapes(LayerDevRecN).insert(text)
    shape.text_size = 0.1/dbu
    t = Trans(Trans.R0, length/9, 0)
    text = Text \
      ('Spice_param:number_of_periods=%s' %\
      (self.number_of_periods1), t )
    shape = shapes(LayerDevRecN).insert(text)
    shape.text_size = 0.1/dbu

    # Create the device recognition layer -- make it 1 * wg_width away from the waveguides.
    t = Trans(Trans.R0, 0,0)
    path = Path([Point(0, 0), Point(length, 0)], 3*w)
    shapes(LayerDevRecN).insert(path.simple_polygon())
    
