#include "MakePdf.h"

////////////////////////////////////////////
RooExtendPdf* MakeExtendedModel(RooWorkspace* workspace, const std::string & label, const std::string & model, const std::string & spectrum, const std::string & channel, const std::string & wtagger_label, std::vector<std::string>* constraint, const int & ismc_wjet, const int & area_init_value){

  std::cout<<" "<<std::endl;
  std::cout<<""<<std::endl;
  std::cout<<"## Make model : "<<label<<" "<<model<<" "<<area_init_value<<" ##"<<std::endl;
  std::cout<<""<<std::endl;
  std::cout<<" "<<std::endl;

  RooRealVar* rrv_number = new  RooRealVar(("rrv_number"+label+"_"+channel+spectrum).c_str(),("rrv_number"+label+"_"+channel+spectrum).c_str(),500.,0.,1e5);
  // call the make RooAbsPdf method
  RooAbsPdf* model_pdf = NULL ;
  model_pdf = MakeGeneralPdf(workspace,label,model,spectrum,wtagger_label,channel,constraint,ismc_wjet);
  // std::cout<< "######## Model Pdf ########"<<std::endl;
  // model_pdf->Print();
      
  // create the extended pdf
  RooExtendPdf* model_extended = new RooExtendPdf(("model"+label+"_"+channel+spectrum).c_str(),("model"+label+"_"+channel+spectrum).c_str(),*model_pdf, *rrv_number);
  std::cout<< "######## Model Extended Pdf ########"<<std::endl;
  // model_extended->Print();
  // return the total extended pdf
  return model_extended;
}

/////////////////////////////


RooGaussian* addConstraint(RooRealVar* rrv_x, double x_mean, double x_sigma, std::vector<std::string>* ConstraintsList){

  //########### Gaussian contraint of a parameter of a pdf
  std::cout<<"########### Add to Constraint List some parameters  ############"<<std::endl;
  RooRealVar* rrv_x_mean  = new RooRealVar((std::string(rrv_x->GetName())+"_mean").c_str() ,(std::string(rrv_x->GetName())+"_mean").c_str() ,x_mean);
  RooRealVar* rrv_x_sigma = new RooRealVar((std::string(rrv_x->GetName())+"_sigma").c_str(),(std::string(rrv_x->GetName())+"_sigma").c_str(),x_sigma);
  RooGaussian* constrainpdf_x = new RooGaussian(("constrainpdf_"+std::string(rrv_x->GetName())).c_str(),("constrainpdf_"+std::string(rrv_x->GetName())).c_str(),*rrv_x,*rrv_x_mean, *rrv_x_sigma);
  //import in the workspace and save the name of constraint pdf
  ConstraintsList->push_back(constrainpdf_x->GetName());
  return constrainpdf_x ;
}

//////////////////

// ---------------------------------------------                                                                                                                                    
RooAbsPdf* MakeModelTTbarControlSample(RooWorkspace* workspace ,const std::string & label, const std::string & modelName, const std::string & spectrum, const std::string & channel, const std::string & wtagger, const std::string & information, std::vector<std::string>* constraint){

  std::cout<<" "<<std::endl;
  std::cout<<"Defining number of real W-jets(rrv_number_total), W-tagging efficiency (eff_ttbar) and total yield after scaling with efficiency (rrv_number)"<<std::endl;
  std::cout<<" Making model for (label, modelName, information) : "<<label<<" "<<modelName<<" "<<information<<" "<<std::endl;
  std::cout<<""<<std::endl;
  std::cout<<" "<<std::endl;

  RooRealVar* rrv_number_total = NULL , *eff_ttbar = NULL ; 
  RooFormulaVar *rrv_number = NULL ;

  if(TString(label).Contains("_ttbar_data") and not TString(label).Contains("failSubjetTau21cut")){
    rrv_number_total = new RooRealVar(("rrv_number_total_ttbar_data"+information+"_"+channel+spectrum).c_str(),("rrv_number_total_ttbar_data"+information+"_"+channel+spectrum).c_str(),500,0.,1e7);
    // eff_ttbar        = new RooRealVar(("eff_ttbar_data"+information+"_"+channel+spectrum).c_str(),("eff_ttbar_data"+information+"_"+channel+spectrum).c_str(),0.7,0.3,0.99);
    eff_ttbar        = new RooRealVar(("eff_ttbar_data"+information+"_"+channel+spectrum).c_str(),("eff_ttbar_data"+information+"_"+channel+spectrum).c_str(),0.7,0.0,0.99);
    rrv_number       = new RooFormulaVar(("rrv_number"+label+"_"+channel+spectrum+spectrum).c_str(), "@0*@1", RooArgList(*rrv_number_total,*eff_ttbar));
  }

  else if(TString(label).Contains("_ttbar_data") and TString(label).Contains("failSubjetTau21cut")){
    rrv_number_total = workspace->var(("rrv_number_total_ttbar_data"+information+"_"+channel+spectrum).c_str());
    eff_ttbar        = workspace->var(("eff_ttbar_data"+information+"_"+channel+spectrum).c_str());
    rrv_number       = new RooFormulaVar(("rrv_number"+label+"_"+channel+spectrum+spectrum).c_str(), "(1-@0)*@1", RooArgList(*eff_ttbar,*rrv_number_total));
  }
  else if(TString(label).Contains("_ttbar_TotalMC") and not TString(label).Contains("failSubjetTau21cut")){
    rrv_number_total = new RooRealVar(("rrv_number_total_ttbar_TotalMC"+information+"_"+channel+spectrum).c_str(),("rrv_number_total_ttbar_TotalMC"+information+"_"+channel+spectrum).c_str(),500,0.,1e7);
    // eff_ttbar        = new RooRealVar(("eff_ttbar_TotalMC"+information+"_"+channel+spectrum).c_str(),("eff_ttbar_TotalMC"+information+"_"+channel+spectrum).c_str(),0.7,0.3,0.99);
    eff_ttbar        = new RooRealVar(("eff_ttbar_TotalMC"+information+"_"+channel+spectrum).c_str(),("eff_ttbar_TotalMC"+information+"_"+channel+spectrum).c_str(),0.7,0.0,0.99);
    rrv_number       = new RooFormulaVar(("rrv_number"+label+"_"+channel+spectrum+spectrum).c_str(), "@0*@1", RooArgList(*eff_ttbar,*rrv_number_total));
  }
  else if(TString(label).Contains("_ttbar_TotalMC") and TString(label).Contains("failSubjetTau21cut")){
    rrv_number_total = workspace->var(("rrv_number_total_ttbar_TotalMC"+information+"_"+channel+spectrum).c_str());
    eff_ttbar        = workspace->var(("eff_ttbar_TotalMC"+information+"_"+channel+spectrum).c_str());
    rrv_number       = new RooFormulaVar(("rrv_number"+label+"_"+channel+spectrum+spectrum).c_str(), "(1-@0)*@1", RooArgList(*eff_ttbar,*rrv_number_total)) ;
  }


  RooAbsPdf* model_pdf = MakeGeneralPdf(workspace,label,modelName,spectrum,wtagger,channel,constraint,false);

  RooExtendPdf* model = new RooExtendPdf(("model"+label+"_"+channel+spectrum).c_str(),("model"+label+"_"+channel+spectrum).c_str(),*model_pdf,*rrv_number);

  workspace->import(*model);
  workspace->pdf(("model"+label+"_"+channel+spectrum).c_str())->Print();
  return workspace->pdf(("model"+label+"_"+channel+spectrum).c_str());

}


//## change a dataset to a histpdf roofit object
void change_dataset_to_histpdf(RooWorkspace* workspace,RooRealVar* x,RooDataSet* dataset){
 
  std::cout<<"######## change the dataset into a histpdf  ########"<<std::endl;
  RooDataHist* datahist = dataset->binnedClone((std::string(dataset->GetName())+"_binnedClone").c_str(),(std::string(dataset->GetName())+"_binnedClone").c_str());
  RooHistPdf* histpdf = new RooHistPdf((std::string(dataset->GetName())+"_histpdf").c_str(),(std::string(dataset->GetName())+"_histpdf").c_str(),RooArgSet(*x),*datahist);
  workspace->import(*histpdf);
}
  
// change from a dataset to a histogramm of Roofit
TH1F* change_dataset_to_histogram(RooRealVar* x, RooDataSet* dataset, const std::string & label, const int & BinWidth){

  std::cout<<"######## change the dataset into a histogramm for mj distribution ########"<<std::endl;
  RooDataHist* datahist = dataset->binnedClone((std::string(dataset->GetName())+"_binnedClone").c_str(),(std::string(dataset->GetName())+"_binnedClone").c_str());
  int nbin = int( (x->getMax()-x->getMin())/BinWidth);
  TString Name ;
  if(label ==""){
    Name.Form("histo_%s",dataset->GetName());
    return (TH1F*) datahist->createHistogram(Name.Data(),*x,RooFit::Binning(nbin,x->getMin(),x->getMax()));
  }
  else{
    Name.Form("histo_%s",label.c_str());
    return (TH1F*) datahist->createHistogram(Name.Data(),*x,RooFit::Binning(nbin,x->getMin(),x->getMax()));
  }

}

////////////////////////////////////

RooAbsPdf* get_mj_Model (RooWorkspace* workspace, const std::string & label, const std::string & channel){
  std::cout<<"model"+label+"_"+channel+"_mj"<<std::endl;
  return workspace->pdf(("model"+label+"_"+channel+"_mj").c_str());

}

RooAbsPdf* get_General_mj_Model(RooWorkspace* workspace, const std::string & label, const std::string & model, const std::string & channel, const int & fix){

  std::cout<<" Fixing and return a general mj model "<<std::endl;
  TString name ;

  if(TString(workspace->GetName()).Contains("4bias")) name.Form("rdataset4bias%s_%s_mj",label.c_str(),channel.c_str());
  else if (TString(workspace->GetName()).Contains("4fit")) name.Form("rdataset%s_%s_mj",label.c_str(),channel.c_str());
  else name.Form("rdataset%s_%s_mj",label.c_str(),channel.c_str());

  RooAbsData* rdataset_General_mj = workspace->data(name.Data());
  RooAbsPdf* model_General = get_mj_Model(workspace,label,channel);
  // rdataset_General_mj->Print();
  // model_General->Print();

  RooArgSet* parameters_General = model_General->getParameters(*rdataset_General_mj);
  TIter par = parameters_General->createIterator(); par.Reset();
  RooRealVar* param = dynamic_cast<RooRealVar*>(par.Next());

  if(fix == 1){
    while(param){
      param->setConstant(kTRUE);
      param->Print();
      param = dynamic_cast<RooRealVar*>(par.Next());
    }
  }
  else if(TString(label).Contains("W")){
    while(param){
      if(TString(param->GetName()).Contains("width")){
        param->setConstant(kTRUE);
        param->Print();
      }
      param = dynamic_cast<RooRealVar*>(par.Next());
    }
  }

  return model_General;
}

RooAbsPdf* get_TTbar_mj_Model  (RooWorkspace* workspace, const std::string & label, const std::string & model, const std::string & channel, const int & fix){

  std::cout<<"########### Fixing TTbar mj model ############"<<std::endl;
  return get_General_mj_Model(workspace,label,model,channel,fix);
}

RooAbsPdf* get_STop_mj_Model  (RooWorkspace* workspace, const std::string & label, const std::string & model, const std::string & channel, const int & fix){

  std::cout<<"########### Fixing STop mj model ############"<<std::endl;
  return get_General_mj_Model(workspace,label,model,channel,fix);
}

RooAbsPdf* get_QCD_mj_Model  (RooWorkspace* workspace, const std::string & label, const std::string & model, const std::string & channel, const int & fix){

  std::cout<<"########### Fixing QCD mj model ############"<<std::endl;
  return get_General_mj_Model(workspace,label,model,channel,fix);
}
 

RooAbsPdf* get_WJets_mj_Model  (RooWorkspace* workspace, const std::string & label, const std::string & model, const std::string & channel, const int & fix, const std::string & jetBin){

  std::cout<<"########### Fixing WJets mj model ############"<<std::endl;
  if(jetBin == "_2jet") return get_General_mj_Model(workspace,label,model,channel,fix);
  else{
    
    TString name ;
    if(TString(workspace->GetName()).Contains("4bias")) name.Form("rdataset4bias%s_%s_mj",label.c_str(),channel.c_str());
    else if (TString(workspace->GetName()).Contains("4fit")) name.Form("rdataset%s_%s_mj",label.c_str(),channel.c_str());
    else name.Form("rdataset%s_%s_mj",label.c_str(),channel.c_str());

    RooDataSet* rdataset_WJets_mj = (RooDataSet*) workspace->data(name.Data());
    // rdataset_WJets_mj->Print();
    RooAbsPdf* model_WJets = get_mj_Model(workspace,label+model,channel);
    // model_WJets->Print();
    RooArgSet* parameters_WJets = model_WJets->getParameters(*rdataset_WJets_mj);
    TIter par = parameters_WJets->createIterator(); par.Reset();
    RooRealVar* param = dynamic_cast<RooRealVar*>(par.Next());
    while (param){
      TString paraName; paraName = Form("%s",param->GetName());
      if (paraName.Contains("rrv_width_ErfExp_WJets") or paraName.Contains("rrv_offset_ErfExp_WJets") or paraName.Contains("rrv_p1_User1_WJets")){
        param->setConstant(kTRUE);
      }
      param =  dynamic_cast<RooRealVar*>(par.Next());
    }
    return model_WJets ;
  }       
   
}

/////////////////////////////////////////

RooAbsPdf* get_mlvj_Model (RooWorkspace* workspace,const std::string & label,const std::string & region,const std::string & model, const std::string & channel){
  //#### get a generic mlvj model from the workspace
  return workspace->pdf(("model"+label+region+model+"_"+channel+"_mlvj").c_str());
}

//#### get a general mlvj model and fiz the paramters --> for extended pdf
RooAbsPdf* get_General_mlvj_Model        (RooWorkspace* workspace,const std::string & label,const std::string & region,const std::string & model, const std::string & channel, const int & fix){
  std::cout<<"Fixing and return a general mlvj model "<<std::endl;
  TString Name ; 
  if(TString(workspace->GetName()).Contains("4bias")) Name.Form("rdataset4bias%s%s_%s_mlvj",label.c_str(),region.c_str(),channel.c_str());
  else if(TString(workspace->GetName()).Contains("4fit")) Name.Form("rdataset%s%s_%s_mlvj",label.c_str(),region.c_str(),channel.c_str());

  RooAbsData* rdataset_General_mlvj = workspace->data(Name.Data());
  RooAbsPdf* model_General = get_mlvj_Model(workspace,label,region,model,channel);
  // rdataset_General_mlvj->Print();
  //   model_General->Print();
  RooArgSet* parameters_General = model_General->getParameters(*rdataset_General_mlvj);
  TIter par = parameters_General->createIterator(); par.Reset();
  RooRealVar* param = dynamic_cast<RooRealVar*>(par.Next());
  if(fix == 1){
    while(param){
      param->setConstant(kTRUE);
      param->Print();
      param = dynamic_cast<RooRealVar*>(par.Next());
    }
  }
  return model_General;
}

//###### get TTbar model mlvj in a region
RooAbsPdf* get_TTbar_mlvj_Model (RooWorkspace* workspace, const std::string & label, const std::string & region, const std::string & model, const std::string & channel, const int & fix){

  std::cout<<"########### Fixing TTbar mlvj model ############"<<std::endl;
  return get_General_mlvj_Model(workspace,label,region,model,channel,fix);
}

//###### get STop model mlvj in a region
RooAbsPdf* get_STop_mlvj_Model (RooWorkspace* workspace, const std::string & label, const std::string & region, const std::string & model, const std::string & channel, const int & fix){

  std::cout<<"########### Fixing STop mlvj model ############"<<std::endl;
  return get_General_mlvj_Model(workspace,label,region,model,channel,fix);
}

//###### get QCD model mlvj in a region
RooAbsPdf* get_QCD_mlvj_Model (RooWorkspace* workspace, const std::string & label,const std::string & region, const std::string & model, const std::string & channel, const int & fix){

  std::cout<<"########### Fixing QCD mlvj model ############"<<std::endl;
  return get_General_mlvj_Model(workspace,label,region,model,channel,fix);
}
 
//###### get Wjets
RooAbsPdf* get_WJets_mlvj_Model  (RooWorkspace* workspace, const std::string & label,const std::string & region,const std::string & model, const std::string & channel, const int & fix){

  std::cout<<"########### Fixing WJets mlvj model ############"<<std::endl;
  return get_General_mlvj_Model(workspace,label,region,model,channel,fix);
}

/////////////////////////////////////////////////
// fix a given model taking the label, and the region --> for extended pdf --> all the parameter of the pdf + normalization
void fix_Model(RooWorkspace* workspace, const std::string & label, const std::string & region, const std::string & spectrum, const std::string & model,const std::string & channel, const std::string & additional_info, const int & notExtended){
  
  RooAbsData* rdataset = NULL ;
  RooAbsPdf* model_pdf = NULL ;             
  std::cout<<"########### Fixing an Extended Pdf for mlvj ############"<<std::endl;
  if(spectrum == "_mj"){  
    TString Name ; Name.Form("rdataset%s%s_%s%s",label.c_str(),region.c_str(),channel.c_str(),spectrum.c_str()); 
    std::cout<<"DataSet Name "<<Name<<std::endl;
    rdataset = workspace->data(Name.Data());
    std::string label2 ; 
    if(notExtended == 1)
      label2 = std::string("_pdf")+label;
    else label2 = label;
    model_pdf = get_mj_Model(workspace,label2+model+additional_info,channel);        
  }
  else{  
    TString Name ; Name.Form("rdataset%s%s_%s%s",label.c_str(),region.c_str(),channel.c_str(),spectrum.c_str());
    std::cout<<"DataSet Name "<<Name<<std::endl;
    rdataset = workspace->data(Name.Data());
    std::string label2 ; 
    if(notExtended == 1)
      label2 = std::string("_pdf")+label;
    else label2 = label;
    model_pdf = get_mlvj_Model(workspace,label2.c_str(),region.c_str(),(model+additional_info).c_str(),channel.c_str());
  }

  // rdataset->Print();
  // model_pdf->Print();
  RooArgSet* parameters = model_pdf->getParameters(*rdataset);
  TIter par = parameters->createIterator(); 
  par.Reset();
  RooRealVar* param = dynamic_cast<RooRealVar*>(par.Next());
  while (param){
    param->setConstant(kTRUE);
    param->Print();       
    param = dynamic_cast<RooRealVar*>(par.Next());
  }
  return ;
}

////////////////////////////////////////////////
void fix_Pdf(RooAbsPdf* model_pdf, RooArgSet* argset_notparameter){

  std::cout<<"########### Fixing a RooAbsPdf for mlvj or mj  ############"<<std::endl;     
  RooArgSet* parameters = model_pdf->getParameters(*argset_notparameter);
  TIter par = parameters->createIterator(); par.Reset();
  RooRealVar* param = dynamic_cast<RooRealVar*>(par.Next());
  while (param){
    param->setConstant(kTRUE);
    param->Print();
    param = dynamic_cast<RooRealVar*>(par.Next());
  }
}

////// print the parameters of a given pdf --> only non constant ones
void ShowParam_Pdf(RooAbsPdf* model_pdf, RooArgSet* argset_notparameter){
 
  std::cout<<"########### Show Parameters of a input model  ############"<<std::endl;        
  model_pdf->Print();
  RooArgSet* parameters = model_pdf->getParameters(*argset_notparameter);
  TIter par = parameters->createIterator(); par.Reset();
  RooRealVar* param = dynamic_cast<RooRealVar*>(par.Next());
  while (param){
    if(not param->isConstant()) param->Print();        
    param = dynamic_cast<RooRealVar*>(par.Next());
  }
}

///////////////////////////////////////////////
RooAbsPdf* MakeGeneralPdf(RooWorkspace* workspace, const std::string & label, const std::string & model, const std::string & spectrum, const std::string & wtagger_label, const std::string & channel, std::vector<std::string>* constraint, const int & ismc){
  
  std::cout<< "Making general PDF for wtagger_label = Hi there"<<wtagger_label.c_str() << " model = "<< model.c_str() << " label = "<< label.c_str()<< " ismc = "<< ismc << " channel = "<< channel.c_str()<< std::endl;

  RooRealVar* rrv_x = NULL ; 
  if(TString(spectrum).Contains("_mj"))   rrv_x = workspace->var("rrv_mass_j");
  if(TString(spectrum).Contains("_mlvj")) rrv_x = workspace->var("rrv_mass_lvj");  
  
  std::cout << "Hi there" << std::endl;
  // Fits for data and MC (not matched tt)
  if( !(TString(label).Contains("realW")) and !(TString(label).Contains("fakeW")) ){
    // ??? exp 
    /*
    if(model == "CB"){
      std::cout<< "########### Cystal Ball for mj fit ############"<<std::endl;
      RooRealVar* rrv_mean_CB  = new RooRealVar(("rrv_mean_CB"+label+"_"+channel+spectrum).c_str(),("rrv_mean_CB"+label+"_"+channel+spectrum).c_str(),84,78,88);
      RooRealVar* rrv_sigma_CB = new RooRealVar(("rrv_sigma_CB"+label+"_"+channel+spectrum).c_str(),("rrv_sigma_CB"+label+"_"+channel+spectrum).c_str(),7,4,10);
      RooRealVar* rrv_alpha_CB = new RooRealVar(("rrv_alpha_CB"+label+"_"+channel+spectrum).c_str(),("rrv_alpha_CB"+label+"_"+channel+spectrum).c_str(),-2,-4,-0.5);
      RooRealVar* rrv_n_CB     = new RooRealVar(("rrv_n_CB"+label+"_"+channel+spectrum).c_str(),("rrv_n_CB"+label+"_"+channel+spectrum).c_str(),2,0.,4);
      RooCBShape* model_pdf = new RooCBShape(("model_pdf"+label+"_"+channel+spectrum).c_str(),("model_pdf"+label+"_"+channel+spectrum).c_str(), *rrv_x,*rrv_mean_CB,*rrv_sigma_CB,*rrv_alpha_CB,*rrv_n_CB);

            
      return model_pdf ;
    }
    */

    if( model == "Exp"){
      std::cout << "Making exp" << std::endl;
      std::cout<< "######### Exp = levelled exp funtion for W+jets mlvj ############" <<std::endl;
      RooRealVar* rrv_c_Exp = new RooRealVar(("rrv_c_Exp"+label+"_"+channel+spectrum).c_str(),("rrv_c_Exp"+label+"_"+channel+spectrum).c_str(),-0.030, -2., 0.05);
      RooExponential* model_pdf_exp = new RooExponential(("model_pdf"+label+"_"+channel+spectrum).c_str(),("model_pdf"+label+"_"+channel+spectrum).c_str(),*rrv_x,*rrv_c_Exp);
      std::cout << "Done" << std::endl;
      return model_pdf_exp ;
    }

    if( model == "Poly5"){
      std::cout << "Making 5th order Polynomial" << std::endl;
      RooRealVar* rrv_polyCo1 = new RooRealVar(("rrv_polyCo1"+label+"_"+channel+spectrum).c_str(),("rrv_polyCo1"+label+"_"+channel+spectrum).c_str(),0., -10., 10.);
      RooRealVar* rrv_polyCo2 = new RooRealVar(("rrv_polyCo2"+label+"_"+channel+spectrum).c_str(),("rrv_polyCo2"+label+"_"+channel+spectrum).c_str(),0., -10., 10.);
      RooRealVar* rrv_polyCo3 = new RooRealVar(("rrv_polyCo3"+label+"_"+channel+spectrum).c_str(),("rrv_polyCo3"+label+"_"+channel+spectrum).c_str(),0., -10., 10.);
      RooRealVar* rrv_polyCo4 = new RooRealVar(("rrv_polyCo4"+label+"_"+channel+spectrum).c_str(),("rrv_polyCo4"+label+"_"+channel+spectrum).c_str(),0., -10., 10.);
      RooRealVar* rrv_polyCo5 = new RooRealVar(("rrv_polyCo5"+label+"_"+channel+spectrum).c_str(),("rrv_polyCo5"+label+"_"+channel+spectrum).c_str(),0., -10., 10.);
   
      RooPolynomial* model_pdf = new RooPolynomial(("model_pdf"+label+"_"+channel+spectrum).c_str(),("model_pdf"+label+"_"+channel+spectrum).c_str(),*rrv_x, RooArgList(*rrv_polyCo1, *rrv_polyCo2, *rrv_polyCo3, *rrv_polyCo4 , *rrv_polyCo5 ));
      std::cout << "Done" << std::endl;
      return model_pdf ;
    }
    /*
    if( model == "Poly5"){
      std::cout << "Making 5th order Polynomial" << std::endl;
       RooRealVar*  poly_coefficient of x^1 ,  10);
    RooRealVar poly_coefficient of x^2 ,  10);
  RooRealVar poly_coefficient of x^3 ,  10);
// Define cubic polynomial PDF
cubic , x, RooArgList(poly_c1, poly_c2, 
		      poly_c3) );polynomialRooPolynomial , polypoly(0, termpoly_, c3c3(0, termpoly_, c2c2(0, termpoly_, c1c1(  

    //RooRealVar* rrv_poly5 = new RooRealVar(("rrv_poly5"+label+"_"+channel+spectrum).c_str(),("rrv_poly5"+label+"_"+channel+spectrum).c_str(),5, 4, 6);
      RooPolynomial* model_pdf = new RooPolynomial(("model_pdf"+label+"_"+channel+spectrum).c_str(),("model_pdf"+label+"_"+channel+spectrum).c_str(),*rrv_x, RooArgList(p1));
      //RooRealVar p1("p1","coeff #1", 100, -1000., 1000.);
      // RooRealVar p2("p2","coeff #2", 10, -100., 100.);
      //RooRealVar p3("p3","coeff #3", 10, -1000., 1000.);
      //RooRealVar p4("p4","coeff #4", 10, -1000., 1000.);
      //RooRealVar p5("p5","coeff #5", 10, -1000., 1000.);
      //RooPolynomial Bkg("bkg","bkgd pdf", x, RooArgList(p1,p2,p3,p4,p5));
      // RooPolynomial Bkg("bkg","bkgd pdf", x, RooArgList(p1));
         
 std::cout << "Done" << std::endl;
      return model_pdf ;
    }
    */




    if( model == "Gaus"){

      std::cout << "Making gaus" << std::endl;
      RooRealVar* rrv_mean2_gaus   = new RooRealVar(("rrv_mean2_gaus"+label+"_"+channel+spectrum).c_str(),("rrv_mean2_gaus"+label+"_"+channel+spectrum).c_str(),86,70,100);
      RooRealVar* rrv_sigma2_gaus  = new RooRealVar(("rrv_sigma2_gaus"+label+"_"+channel+spectrum).c_str(),("rrv_sigma2_gaus"+label+"_"+channel+spectrum).c_str(),9,7.,35);  

      /*
      if( TString(wtagger_label.c_str()).Contains("200Toinf") and TString(label).Contains("bkg") ){
	std::cout<<"For this 200-Infinity pt bin the model is  "<<  model << "and tstring is"<< wtagger_label.c_str()    << std::endl;

        RooRealVar* rrv_mean1_gaus   = new RooRealVar(("rrv_mean1_gaus"+label+"_"+channel+spectrum).c_str(),("rrv_mean1_gaus"+label+"_"+channel+spectrum).c_str(),83,75,87);
        RooRealVar* rrv_sigma1_gaus  = new RooRealVar(("rrv_sigma1_gaus"+label+"_"+channel+spectrum).c_str(),("rrv_sigma1_gaus"+label+"_"+channel+spectrum).c_str(),20,12.,40);

      }
      

      if(TString(wtagger_label.c_str()).Contains("HP0v40")){

	if(TString(wtagger_label.c_str()).Contains("300To500")){
	  std::cout<<"Model used for 300-500 Medium WP 0.40 is "<<  model << "and tstring containing bkg is "<< wtagger_label.c_str()    << std::endl;
          rrv_mean1_gaus  = new RooRealVar(("rrv_mean1_gaus"+label+"_"+channel+spectrum).c_str(),("rrv_mean1_gaus"+label+"_"+channel+spectrum).c_str(),89,86.,95.);
          rrv_sigma1_gaus  = new RooRealVar(("rrv_sigma1_gaus"+label+"_"+channel+spectrum).c_str(),("rrv_sigma1_gaus"+label+"_"+channel+spectrum).c_str(), 8. , 4., 17. );
          if ( TString(label).Contains("bkg")){ // WORKING HERE July 3rd 2017 ???? !!!!
	    rrv_mean1_gaus  = new RooRealVar(("rrv_mean1_gaus"+label+"_"+channel+spectrum).c_str(),("rrv_mean1_gaus"+label+"_"+channel+spectrum).c_str(),89,86.,95.);
	    rrv_sigma1_gaus  = new RooRealVar(("rrv_sigma1_gaus"+label+"_"+channel+spectrum).c_str(),("rrv_sigma1_gaus"+label+"_"+channel+spectrum).c_str(), 8. , 4., 17. );  
          }// end bkg 

     
        }//end 300-500


      }//end medium WP 0.4 tau21 cut
      */
      if( TString(wtagger_label.c_str()).Contains("500Toinf") and TString(label).Contains("bkg") ){
	std::cout<<"For this 500-Infinity pt bin the signal model is  "<<  model << "and tstring is "<< wtagger_label.c_str()    << std::endl;

	RooRealVar* rrv_mean2_gaus   = new RooRealVar(("rrv_mean2_gaus"+label+"_"+channel+spectrum).c_str(),("rrv_mean2_gaus"+label+"_"+channel+spectrum).c_str(),87,65,90);
        RooRealVar* rrv_sigma2_gaus  = new RooRealVar(("rrv_sigma2_gaus"+label+"_"+channel+spectrum).c_str(),("rrv_sigma2_gaus"+label+"_"+channel+spectrum).c_str(),12,12.,55);

      } 


      RooGaussian* model_pdf       = new RooGaussian(("gaus"+label+"_"+channel+spectrum).c_str(),("gaus"+label+"_"+channel+spectrum).c_str(), *rrv_x,*rrv_mean2_gaus,*rrv_sigma2_gaus);
      std::cout << "Done" << std::endl;
      return model_pdf ;
    }
    
    if( model == "Gaus_SigFail"){

      std::cout << "Making gaus for signal fail" << std::endl;
      RooRealVar* rrv_mean1a_gaus   = new RooRealVar(("rrv_mean1a_gaus"+label+"_"+channel+spectrum).c_str(),("rrv_mean1a_gaus"+label+"_"+channel+spectrum).c_str(),70,65,95);
      RooRealVar* rrv_sigma1a_gaus  = new RooRealVar(("rrv_sigma1a_gaus"+label+"_"+channel+spectrum).c_str(),("rrv_sigma1a_gaus"+label+"_"+channel+spectrum).c_str(),8.33 ,7.,35);
      RooGaussian* model_pdf       = new RooGaussian(("gaus1"+label+"_"+channel+spectrum).c_str(),("gaus1"+label+"_"+channel+spectrum).c_str(), *rrv_x,*rrv_mean1a_gaus,*rrv_sigma1a_gaus);
      std::cout << "Done" << std::endl;
      return model_pdf ;
    }

    if( model == "Gaus_Sig"){

      std::cout << "Making gaus for signal fail" << std::endl;
      RooRealVar* rrv_mean1ap_gaus   = new RooRealVar(("rrv_mean1ap_gaus"+label+"_"+channel+spectrum).c_str(),("rrv_mean1ap_gaus"+label+"_"+channel+spectrum).c_str(),90,70,100);
      RooRealVar* rrv_sigma1ap_gaus  = new RooRealVar(("rrv_sigma1ap_gaus"+label+"_"+channel+spectrum).c_str(),("rrv_sigma1ap_gaus"+label+"_"+channel+spectrum).c_str(),12.33 ,7.,15);
      RooGaussian* model_pdf       = new RooGaussian(("gaus1"+label+"_"+channel+spectrum).c_str(),("gaus1"+label+"_"+channel+spectrum).c_str(), *rrv_x,*rrv_mean1ap_gaus,*rrv_sigma1ap_gaus);
      std::cout << "Done" << std::endl;
      return model_pdf ;
    }

    if( model == "Gaus_QCD"){

      std::cout << "Making gaus" << std::endl;
      RooRealVar* rrv_mean1_gaus   = new RooRealVar(("rrv_mean1_gaus"+label+"_"+channel+spectrum).c_str(),("rrv_mean1_gaus"+label+"_"+channel+spectrum).c_str(),57,45,65);
      RooRealVar* rrv_sigma1_gaus  = new RooRealVar(("rrv_sigma1_gaus"+label+"_"+channel+spectrum).c_str(),("rrv_sigma1_gaus"+label+"_"+channel+spectrum).c_str(),22.33 ,10.,55);
      RooGaussian* model_pdf       = new RooGaussian(("gaus"+label+"_"+channel+spectrum).c_str(),("gaus"+label+"_"+channel+spectrum).c_str(), *rrv_x,*rrv_mean1_gaus,*rrv_sigma1_gaus);
      std::cout << "Done" << std::endl;
      return model_pdf ;
    }

    if( model == "Gaus_bkg"){

      std::cout << "Making gaus" << std::endl;
      RooRealVar* rrv_mean1_gaus   = new RooRealVar(("rrv_mean1_gaus"+label+"_"+channel+spectrum).c_str(),("rrv_mean1_gaus"+label+"_"+channel+spectrum).c_str(),57,45,60);
      RooRealVar* rrv_sigma1_gaus  = new RooRealVar(("rrv_sigma1_gaus"+label+"_"+channel+spectrum).c_str(),("rrv_sigma1_gaus"+label+"_"+channel+spectrum).c_str(),22.33 ,10.,55);
      RooGaussian* model_pdf       = new RooGaussian(("gaus"+label+"_"+channel+spectrum).c_str(),("gaus"+label+"_"+channel+spectrum).c_str(), *rrv_x,*rrv_mean1_gaus,*rrv_sigma1_gaus);
      std::cout << "Done" << std::endl;
      return model_pdf ;
    }

    if( model == "Landau"){

      std::cout << "Making Landau" << std::endl;

      RooRealVar* rrv_mean1_lan   = new RooRealVar(("rrv_mean1_lan"+label+"_"+channel+spectrum).c_str(),("rrv_mean1_lan"+label+"_"+channel+spectrum).c_str(),50,35,110);
      RooRealVar* rrv_sigma1_lan  = new RooRealVar(("rrv_sigma1_lan"+label+"_"+channel+spectrum).c_str(),("rrv_sigma1_lan"+label+"_"+channel+spectrum).c_str(),15.33 ,6.,55);
      RooGaussian* model_pdf       = new RooGaussian(("landau"+label+"_"+channel+spectrum).c_str(),("landau"+label+"_"+channel+spectrum).c_str(), *rrv_x,*rrv_mean1_lan,*rrv_sigma1_lan);
      std::cout << "Done" << std::endl;
      return model_pdf ;
    }


    if( model == "DeuxGaus"){
      double frac_tmp = 0.3;

      std::cout << "Making gaus0" << std::endl;
      //   RooRealVar* rrv_mean0_gaus   = new RooRealVar(("rrv_mean0_gaus"+label+"_"+channel+spectrum).c_str(),("rrv_mean1_gaus"+label+"_"+channel+spectrum).c_str(),91,91,110);
      // RooRealVar* rrv_sigma0_gaus  = new RooRealVar(("rrv_sigma0_gaus"+label+"_"+channel+spectrum).c_str(),("rrv_sigma1_gaus"+label+"_"+channel+spectrum).c_str(),7.,5.,15);
      //RooGaussian* model_pdf       = new RooGaussian(("gaus"+label+"_"+channel+spectrum).c_str(),("gaus"+label+"_"+channel+spectrum).c_str(), *rrv_x,*rrv_mean0_gaus,*rrv_sigma0_gaus);
      RooRealVar* rrv_mean0_gaus   = new RooRealVar(("rrv_mean0_gaus"+label+"_"+channel+spectrum).c_str(),("rrv_mean1_gaus"+label+"_"+channel+spectrum).c_str(),85,75,94);
      RooRealVar* rrv_sigma0_gaus  = new RooRealVar(("rrv_sigma0_gaus"+label+"_"+channel+spectrum).c_str(),("rrv_sigma1_gaus"+label+"_"+channel+spectrum).c_str(),12,5,14);
     
      std::cout << "Done" << std::endl;
      std::cout << "Making gaus1" << std::endl;
      RooRealVar* rrv_mean1_gaus   = new RooRealVar(("rrv_mean1_gaus"+label+"_"+channel+spectrum).c_str(),("rrv_mean1_gaus"+label+"_"+channel+spectrum).c_str(),50,45,59);
      RooRealVar* rrv_sigma1_gaus  = new RooRealVar(("rrv_sigma1_gaus"+label+"_"+channel+spectrum).c_str(),("rrv_sigma1_gaus"+label+"_"+channel+spectrum).c_str(),12,4.,35);

      //      RooRealVar* rrv_mean1_gaus   = new RooRealVar(("rrv_mean1_gaus"+label+"_"+channel+spectrum).c_str(),("rrv_mean1_gaus"+label+"_"+channel+spectrum).c_str(),50,50,165);
      // RooRealVar* rrv_sigma1_gaus  = new RooRealVar(("rrv_sigma1_gaus"+label+"_"+channel+spectrum).c_str(),("rrv_sigma1_gaus"+label+"_"+channel+spectrum).c_str(),30,18.,70);
      std::cout << "Done" << std::endl;
      if( TString(wtagger_label.c_str()).Contains("200Toinf")  ){
	std::cout<<"For this 200-Infinity pt bin the model is  "<<  model << "and tstring is"<< wtagger_label.c_str()    << std::endl;
	RooRealVar* rrv_mean0_gaus   = new RooRealVar(("rrv_mean0_gaus"+label+"_"+channel+spectrum).c_str(),("rrv_mean1_gaus"+label+"_"+channel+spectrum).c_str(),75,72,80);
	RooRealVar* rrv_sigma0_gaus  = new RooRealVar(("rrv_sigma0_gaus"+label+"_"+channel+spectrum).c_str(),("rrv_sigma1_gaus"+label+"_"+channel+spectrum).c_str(),12.,9.,100);
	RooRealVar* rrv_mean1_gaus   = new RooRealVar(("rrv_mean1_gaus"+label+"_"+channel+spectrum).c_str(),("rrv_mean1_gaus"+label+"_"+channel+spectrum).c_str(),50,43,55);
	RooRealVar* rrv_sigma1_gaus  = new RooRealVar(("rrv_sigma1_gaus"+label+"_"+channel+spectrum).c_str(),("rrv_sigma1_gaus"+label+"_"+channel+spectrum).c_str(),30,12.,100);
    
        }
      /*
      if( TString(wtagger_label.c_str()).Contains("500Toinf")  ){
	std::cout<<"For this 500-Infinity pt bin the model is  "<<  model << "and tstring is"<< wtagger_label.c_str()    << std::endl;
        RooRealVar* rrv_mean0_gaus   = new RooRealVar(("rrv_mean0_gaus"+label+"_"+channel+spectrum).c_str(),("rrv_mean1_gaus"+label+"_"+channel+spectrum).c_str(),90,86,100);
        RooRealVar* rrv_sigma0_gaus  = new RooRealVar(("rrv_sigma0_gaus"+label+"_"+channel+spectrum).c_str(),("rrv_sigma1_gaus"+label+"_"+channel+spectrum).c_str(),12,7,22);
        RooRealVar* rrv_mean1_gaus   = new RooRealVar(("rrv_mean1_gaus"+label+"_"+channel+spectrum).c_str(),("rrv_mean1_gaus"+label+"_"+channel+spectrum).c_str(),110,90,130);
        RooRealVar* rrv_sigma1_gaus  = new RooRealVar(("rrv_sigma1_gaus"+label+"_"+channel+spectrum).c_str(),("rrv_sigma1_gaus"+label+"_"+channel+spectrum).c_str(),20,12.,100);

      }
      */

      // OPTIMIZED FOR PYTHIA8 MC                                                                                                                                                                                                                   
      if(TString(wtagger_label.c_str()).Contains("500Toinf") ) {
	RooRealVar* rrv_c_Exp       = new RooRealVar(("rrv_c_Exp"+label+"_"+channel+spectrum).c_str(),("rrv_c_Exp"+label+"_"+channel+spectrum).c_str(),-0.05,-2.,0.99);
	if (TString(label.c_str()).Contains("bkg") and !TString(label.c_str()).Contains("fail")){
	  std::cout<<"For this 500-inf pt bin the model forpass bkg is  "<<  model << "and tstring is"<< wtagger_label.c_str()    << std::endl;
	  rrv_mean1_gaus  = new RooRealVar(("rrv_mean1_gaus"+label+"_"+channel+spectrum).c_str(),("rrv_mean1_gaus"+label+"_"+channel+spectrum).c_str(),89,67.,119.2 );
	  rrv_sigma1_gaus  = new RooRealVar(("rrv_sigma1_gaus"+label+"_"+channel+spectrum).c_str(),("rrv_sigma1_gaus"+label+"_"+channel+spectrum).c_str(), 9.33 , 9.55, 16. );                                                   
	} // end if bkg pass                                                                                                                                                                                                                     
	if (!TString(label.c_str()).Contains("bkg") and !TString(label.c_str()).Contains("fail")){
	  if (TString(label.c_str()).Contains("_data_")){
	    std::cout<<"For this 500-inf pt bin the model for data signal pass is  "<<  model << "and tstring is"<< wtagger_label.c_str()    << std::endl;

	    RooRealVar* rrv_mean0_gaus   = new RooRealVar(("rrv_mean0_gaus"+label+"_"+channel+spectrum).c_str(),("rrv_mean1_gaus"+label+"_"+channel+spectrum).c_str(), 86,84,95);
            RooRealVar* rrv_sigma0_gaus  = new RooRealVar(("rrv_sigma0_gaus"+label+"_"+channel+spectrum).c_str(),("rrv_sigma1_gaus"+label+"_"+channel+spectrum).c_str(),12,10,32);
	    RooRealVar* rrv_mean1_gaus   = new RooRealVar(("rrv_mean1_gaus"+label+"_"+channel+spectrum).c_str(),("rrv_mean1_gaus"+label+"_"+channel+spectrum).c_str(),125,90,130);
	    RooRealVar* rrv_sigma1_gaus  = new RooRealVar(("rrv_sigma1_gaus"+label+"_"+channel+spectrum).c_str(),("rrv_sigma1_gaus"+label+"_"+channel+spectrum).c_str(),26,25.,100);

	  }
	  if (TString(label.c_str()).Contains("_TotalMC_")){
	    std::cout<<"For this 500-inf pt bin the model for MC signal pass is  "<<  model << "and tstring is"<< wtagger_label.c_str()    << std::endl;
	    // RooRealVar* rrv_mean0_gaus   = new RooRealVar(("rrv_mean0_gaus"+label+"_"+channel+spectrum).c_str(),("rrv_mean1_gaus"+label+"_"+channel+spectrum).c_str(),91,91,110);
	    //RooRealVar* rrv_sigma0_gaus  = new RooRealVar(("rrv_sigma0_gaus"+label+"_"+channel+spectrum).c_str(),("rrv_sigma1_gaus"+label+"_"+channel+spectrum).c_str(),12,7,22);
	    // RooRealVar* rrv_mean1_gaus   = new RooRealVar(("rrv_mean1_gaus"+label+"_"+channel+spectrum).c_str(),("rrv_mean1_gaus"+label+"_"+channel+spectrum).c_str(),110,90,130);
	    //RooRealVar* rrv_sigma1_gaus  = new RooRealVar(("rrv_sigma1_gaus"+label+"_"+channel+spectrum).c_str(),("rrv_sigma1_gaus"+label+"_"+channel+spectrum).c_str(),26,25.,100);
	    RooRealVar* rrv_mean0_gaus   = new RooRealVar(("rrv_mean0_gaus"+label+"_"+channel+spectrum).c_str(),("rrv_mean1_gaus"+label+"_"+channel+spectrum).c_str(),81,71,87);
	    RooRealVar* rrv_sigma0_gaus  = new RooRealVar(("rrv_sigma0_gaus"+label+"_"+channel+spectrum).c_str(),("rrv_sigma1_gaus"+label+"_"+channel+spectrum).c_str(),8,7,9);//13);                           
	    RooRealVar* rrv_mean1_gaus   = new RooRealVar(("rrv_mean1_gaus"+label+"_"+channel+spectrum).c_str(),("rrv_mean1_gaus"+label+"_"+channel+spectrum).c_str(),110,90,130);
	    RooRealVar* rrv_sigma1_gaus  = new RooRealVar(("rrv_sigma1_gaus"+label+"_"+channel+spectrum).c_str(),("rrv_sigma1_gaus"+label+"_"+channel+spectrum).c_str(),26,15.,45. );//100);                      

	  }

	} // end if signal pass                                                                                                                                                                                                                 
	if (!TString(label.c_str()).Contains("bkg") and TString(label.c_str()).Contains("fail")){
	 
          if (TString(label.c_str()).Contains("_data_")){
	    std::cout<<"For this 500-inf pt bin the model for data signal fail is  "<<  model << "and tstring is"<< wtagger_label.c_str()    << std::endl;

            RooRealVar* rrv_mean0_gaus   = new RooRealVar(("rrv_mean0_gaus"+label+"_"+channel+spectrum).c_str(),("rrv_mean1_gaus"+label+"_"+channel+spectrum).c_str(),85,81,95);
            RooRealVar* rrv_sigma0_gaus  = new RooRealVar(("rrv_sigma0_gaus"+label+"_"+channel+spectrum).c_str(),("rrv_sigma1_gaus"+label+"_"+channel+spectrum).c_str(),12,5,26);
            RooRealVar* rrv_mean1_gaus   = new RooRealVar(("rrv_mean1_gaus"+label+"_"+channel+spectrum).c_str(),("rrv_mean1_gaus"+label+"_"+channel+spectrum).c_str(),45,40,65);
            RooRealVar* rrv_sigma1_gaus  = new RooRealVar(("rrv_sigma1_gaus"+label+"_"+channel+spectrum).c_str(),("rrv_sigma1_gaus"+label+"_"+channel+spectrum).c_str(),12,7.,22);

          }
          if (TString(label.c_str()).Contains("_TotalMC_")){
	      std::cout<<"For this 500-inf pt bin the model for MC signal fail is  "<<  model << "and tstring is "<< wtagger_label.c_str()    << std::endl;
            RooRealVar* rrv_mean0_gaus   = new RooRealVar(("rrv_mean0_gaus"+label+"_"+channel+spectrum).c_str(),("rrv_mean1_gaus"+label+"_"+channel+spectrum).c_str(),83,75,90);
            RooRealVar* rrv_sigma0_gaus  = new RooRealVar(("rrv_sigma0_gaus"+label+"_"+channel+spectrum).c_str(),("rrv_sigma1_gaus"+label+"_"+channel+spectrum).c_str(),12,7,18);
            RooRealVar* rrv_mean1_gaus   = new RooRealVar(("rrv_mean1_gaus"+label+"_"+channel+spectrum).c_str(),("rrv_mean1_gaus"+label+"_"+channel+spectrum).c_str(),52,40,60);
            RooRealVar* rrv_sigma1_gaus  = new RooRealVar(("rrv_sigma1_gaus"+label+"_"+channel+spectrum).c_str(),("rrv_sigma1_gaus"+label+"_"+channel+spectrum).c_str(),12,7.,19);


          }

	} // end if signal fail                                                                                                                                                                                                                  
	if (TString(label.c_str()).Contains("bkg") and TString(label.c_str()).Contains("fail")){

	  //	  RooRealVar* rrv_mean0_gaus   = new RooRealVar(("rrv_mean0_gaus"+label+"_"+channel+spectrum).c_str(),("rrv_mean1_gaus"+label+"_"+channel+spectrum).c_str(),95,91,100);
	  // RooRealVar* rrv_sigma0_gaus  = new RooRealVar(("rrv_sigma0_gaus"+label+"_"+channel+spectrum).c_str(),("rrv_sigma1_gaus"+label+"_"+channel+spectrum).c_str(),12,7,22);
	  // RooRealVar* rrv_mean1_gaus   = new RooRealVar(("rrv_mean1_gaus"+label+"_"+channel+spectrum).c_str(),("rrv_mean1_gaus"+label+"_"+channel+spectrum).c_str(),110,90,130);
	  // RooRealVar* rrv_sigma1_gaus  = new RooRealVar(("rrv_sigma1_gaus"+label+"_"+channel+spectrum).c_str(),("rrv_sigma1_gaus"+label+"_"+channel+spectrum).c_str(),20,12.,100);




	} // end if bkg fail                                                                                                                                                                                                                     

	if( (TString(label).Contains("_STop" ) or TString(label).Contains("_W" )  or TString(label).Contains("_QCD" ) ) and !TString(label).Contains("failSubjetTau21cut" )  ) {
	  //rrv_c_Exp       = new RooRealVar(("rrv_c_Exp"+label+"_"+channel+spectrum).c_str(),("rrv_c_Exp"+label+"_"+channel+spectrum).c_str(),-0.03,-0.5,0.5);                                                                                  
	  RooRealVar* rrv_mean0_gaus   = new RooRealVar(("rrv_mean0_gaus"+label+"_"+channel+spectrum).c_str(),("rrv_mean1_gaus"+label+"_"+channel+spectrum).c_str(),95,91,100);
	  RooRealVar* rrv_sigma0_gaus  = new RooRealVar(("rrv_sigma0_gaus"+label+"_"+channel+spectrum).c_str(),("rrv_sigma1_gaus"+label+"_"+channel+spectrum).c_str(),12,7,22);
	  RooRealVar* rrv_mean1_gaus   = new RooRealVar(("rrv_mean1_gaus"+label+"_"+channel+spectrum).c_str(),("rrv_mean1_gaus"+label+"_"+channel+spectrum).c_str(),110,90,130);
	  RooRealVar* rrv_sigma1_gaus  = new RooRealVar(("rrv_sigma1_gaus"+label+"_"+channel+spectrum).c_str(),("rrv_sigma1_gaus"+label+"_"+channel+spectrum).c_str(),20,12.,100);




	}


      } // end if 500-inf     



      RooGaussian* gaus0 = new RooGaussian(("gaus0"+label+"_"+channel+spectrum).c_str(),("gaus0"+label+"_"+channel+spectrum).c_str(), *rrv_x,*rrv_mean0_gaus,*rrv_sigma0_gaus); 
      RooGaussian* gaus1 = new RooGaussian(("gaus1"+label+"_"+channel+spectrum).c_str(),("gaus1"+label+"_"+channel+spectrum).c_str(), *rrv_x,*rrv_mean1_gaus,*rrv_sigma1_gaus);                                                        
      std::cout<< "######## Testing 1,2 ########"<<std::endl;                                                                                                                                                                          
      RooRealVar* rrv_frac1 = new RooRealVar(("rrv_frac1"+label+"_"+channel+spectrum).c_str(),("rrv_frac1"+label+"_"+channel+spectrum).c_str(),frac_tmp,0,1);     

      std::cout<< "######## Testing 1,2,3. ########"<<std::endl;                                                                                                                     
      RooAddPdf* model_pdf = new RooAddPdf(("model_pdf"+label+"_"+channel+spectrum).c_str(),("model_pdf"+label+"_"+channel+spectrum).c_str(),RooArgList(*gaus0,*gaus1),RooArgList(*rrv_frac1),1);                                      
        

      return model_pdf ;
    }




    if( model == "DeuxGausExp"){
      double frac_tmp = 0.3;

      std::cout << "Making gaus0" << std::endl;
      RooRealVar* rrv_mean0_gaus   = new RooRealVar(("rrv_mean0_gaus"+label+"_"+channel+spectrum).c_str(),("rrv_mean1_gaus"+label+"_"+channel+spectrum).c_str(),95,93,150);
      RooRealVar* rrv_sigma0_gaus  = new RooRealVar(("rrv_sigma0_gaus"+label+"_"+channel+spectrum).c_str(),("rrv_sigma1_gaus"+label+"_"+channel+spectrum).c_str(),7.,5.,18.33 );
      //RooGaussian* model_pdf       = new RooGaussian(("gaus"+label+"_"+channel+spectrum).c_str(),("gaus"+label+"_"+channel+spectrum).c_str(), *rrv_x,*rrv_mean0_gaus,*rrv_sigma0_gaus);                                                                                                                                                                                                                                      

      std::cout << "Done" << std::endl;
      std::cout << "Making gaus1" << std::endl;
      RooRealVar* rrv_mean1_gaus   = new RooRealVar(("rrv_mean1_gaus"+label+"_"+channel+spectrum).c_str(),("rrv_mean1_gaus"+label+"_"+channel+spectrum).c_str(),125,93,140);
      RooRealVar* rrv_sigma1_gaus  = new RooRealVar(("rrv_sigma1_gaus"+label+"_"+channel+spectrum).c_str(),("rrv_sigma1_gaus"+label+"_"+channel+spectrum).c_str(),30,22.,40);
      std::cout << "Done" << std::endl;
      if( TString(wtagger_label.c_str()).Contains("200Toinf")  ){
	std::cout<<"For this 200-Infinity pt bin the model is  "<<  model << "and tstring is"<< wtagger_label.c_str()    << std::endl;
        RooRealVar* rrv_mean0_gaus   = new RooRealVar(("rrv_mean0_gaus"+label+"_"+channel+spectrum).c_str(),("rrv_mean1_gaus"+label+"_"+channel+spectrum).c_str(),75,72,80);
        RooRealVar* rrv_sigma0_gaus  = new RooRealVar(("rrv_sigma0_gaus"+label+"_"+channel+spectrum).c_str(),("rrv_sigma1_gaus"+label+"_"+channel+spectrum).c_str(),12.,9.,100);
        RooRealVar* rrv_mean1_gaus   = new RooRealVar(("rrv_mean1_gaus"+label+"_"+channel+spectrum).c_str(),("rrv_mean1_gaus"+label+"_"+channel+spectrum).c_str(),50,43,55);
        RooRealVar* rrv_sigma1_gaus  = new RooRealVar(("rrv_sigma1_gaus"+label+"_"+channel+spectrum).c_str(),("rrv_sigma1_gaus"+label+"_"+channel+spectrum).c_str(),30,12.,100);

      }


      // OPTIMIZED FOR PYTHIA8 MC                                                                                                                                                                                                                                                                                                                                   
      if(TString(wtagger_label.c_str()).Contains("500Toinf") ) {
        RooRealVar* rrv_c_Exp       = new RooRealVar(("rrv_c_Exp"+label+"_"+channel+spectrum).c_str(),("rrv_c_Exp"+label+"_"+channel+spectrum).c_str(),-0.05,-2.,0.99);
	if (TString(label.c_str()).Contains("bkg") and !TString(label.c_str()).Contains("fail")){
	  std::cout<<"For this 500-inf pt bin the model forpass bkg is  "<<  model << "and tstring is"<< wtagger_label.c_str()    << std::endl;
	  RooRealVar* rrv_mean0_gaus   = new RooRealVar(("rrv_mean0_gaus"+label+"_"+channel+spectrum).c_str(),("rrv_mean1_gaus"+label+"_"+channel+spectrum).c_str(),93,95.,130);
	  RooRealVar* rrv_sigma0_gaus  = new RooRealVar(("rrv_sigma0_gaus"+label+"_"+channel+spectrum).c_str(),("rrv_sigma1_gaus"+label+"_"+channel+spectrum).c_str(),12,10,32);
	  RooRealVar* rrv_mean1_gaus   = new RooRealVar(("rrv_mean1_gaus"+label+"_"+channel+spectrum).c_str(),("rrv_mean1_gaus"+label+"_"+channel+spectrum).c_str(),125,95,130);
	  RooRealVar* rrv_sigma1_gaus  = new RooRealVar(("rrv_sigma1_gaus"+label+"_"+channel+spectrum).c_str(),("rrv_sigma1_gaus"+label+"_"+channel+spectrum).c_str(),26,25.,100);

       
        
        } // end if bkg pass                                                                                                                                                                                                                                                                                                                                        
        if (!TString(label.c_str()).Contains("bkg") and !TString(label.c_str()).Contains("fail")){
          if (TString(label.c_str()).Contains("_data_")){
	    std::cout<<"For this 500-inf pt bin the model for data signal pass is  "<<  model << "and tstring is"<< wtagger_label.c_str()    << std::endl;

            RooRealVar* rrv_mean0_gaus   = new RooRealVar(("rrv_mean0_gaus"+label+"_"+channel+spectrum).c_str(),("rrv_mean1_gaus"+label+"_"+channel+spectrum).c_str(),93,95.,130);
            RooRealVar* rrv_sigma0_gaus  = new RooRealVar(("rrv_sigma0_gaus"+label+"_"+channel+spectrum).c_str(),("rrv_sigma1_gaus"+label+"_"+channel+spectrum).c_str(),12,10,32);
            RooRealVar* rrv_mean1_gaus   = new RooRealVar(("rrv_mean1_gaus"+label+"_"+channel+spectrum).c_str(),("rrv_mean1_gaus"+label+"_"+channel+spectrum).c_str(),125,95,130);
            RooRealVar* rrv_sigma1_gaus  = new RooRealVar(("rrv_sigma1_gaus"+label+"_"+channel+spectrum).c_str(),("rrv_sigma1_gaus"+label+"_"+channel+spectrum).c_str(),26,25.,100);

          }
          if (TString(label.c_str()).Contains("_TotalMC_")){
	    std::cout<<"For this 500-inf pt bin the model for MC signal pass is  "<<  model << "and tstring is"<< wtagger_label.c_str()    << std::endl;
            RooRealVar* rrv_mean0_gaus   = new RooRealVar(("rrv_mean0_gaus"+label+"_"+channel+spectrum).c_str(),("rrv_mean1_gaus"+label+"_"+channel+spectrum).c_str(),95,93,110);
            RooRealVar* rrv_sigma0_gaus  = new RooRealVar(("rrv_sigma0_gaus"+label+"_"+channel+spectrum).c_str(),("rrv_sigma1_gaus"+label+"_"+channel+spectrum).c_str(),12,7,22);
            RooRealVar* rrv_mean1_gaus   = new RooRealVar(("rrv_mean1_gaus"+label+"_"+channel+spectrum).c_str(),("rrv_mean1_gaus"+label+"_"+channel+spectrum).c_str(),110,93,130);
            RooRealVar* rrv_sigma1_gaus  = new RooRealVar(("rrv_sigma1_gaus"+label+"_"+channel+spectrum).c_str(),("rrv_sigma1_gaus"+label+"_"+channel+spectrum).c_str(),26,25.,100);


          }

        } // end if signal pass                                                                                                                                                                                                                                                                                                                                     
        if (!TString(label.c_str()).Contains("bkg") and TString(label.c_str()).Contains("fail")){

          if (TString(label.c_str()).Contains("_data_")){
	    std::cout<<"For this 500-inf pt bin the model for data signal fail is  "<<  model << "and tstring is"<< wtagger_label.c_str()    << std::endl;

            RooRealVar* rrv_mean0_gaus   = new RooRealVar(("rrv_mean0_gaus"+label+"_"+channel+spectrum).c_str(),("rrv_mean1_gaus"+label+"_"+channel+spectrum).c_str(),85,71,95);
            RooRealVar* rrv_sigma0_gaus  = new RooRealVar(("rrv_sigma0_gaus"+label+"_"+channel+spectrum).c_str(),("rrv_sigma1_gaus"+label+"_"+channel+spectrum).c_str(),12,10,22);
            RooRealVar* rrv_mean1_gaus   = new RooRealVar(("rrv_mean1_gaus"+label+"_"+channel+spectrum).c_str(),("rrv_mean1_gaus"+label+"_"+channel+spectrum).c_str(),45,40,55);
            RooRealVar* rrv_sigma1_gaus  = new RooRealVar(("rrv_sigma1_gaus"+label+"_"+channel+spectrum).c_str(),("rrv_sigma1_gaus"+label+"_"+channel+spectrum).c_str(),12,7.,22);

          }
          if (TString(label.c_str()).Contains("_TotalMC_")){
	    std::cout<<"For this 500-inf pt bin the model for MC signal fail is  "<<  model << "and tstring is "<< wtagger_label.c_str()    << std::endl;
            RooRealVar* rrv_mean0_gaus   = new RooRealVar(("rrv_mean0_gaus"+label+"_"+channel+spectrum).c_str(),("rrv_mean1_gaus"+label+"_"+channel+spectrum).c_str(),85,75,90);
            RooRealVar* rrv_sigma0_gaus  = new RooRealVar(("rrv_sigma0_gaus"+label+"_"+channel+spectrum).c_str(),("rrv_sigma1_gaus"+label+"_"+channel+spectrum).c_str(),12,7,18);
            RooRealVar* rrv_mean1_gaus   = new RooRealVar(("rrv_mean1_gaus"+label+"_"+channel+spectrum).c_str(),("rrv_mean1_gaus"+label+"_"+channel+spectrum).c_str(),52,45,55);
            RooRealVar* rrv_sigma1_gaus  = new RooRealVar(("rrv_sigma1_gaus"+label+"_"+channel+spectrum).c_str(),("rrv_sigma1_gaus"+label+"_"+channel+spectrum).c_str(),12,7.,19);


          }





	  /*
          if (TString(label.c_str()).Contains("_data_")){
	    std::cout<<"For this 500-inf pt bin the model for data signal fail is  "<<  model << "and tstring is"<< wtagger_label.c_str()    << std::endl;

            RooRealVar* rrv_mean0_gaus   = new RooRealVar(("rrv_mean0_gaus"+label+"_"+channel+spectrum).c_str(),("rrv_mean1_gaus"+label+"_"+channel+spectrum).c_str(),94,93,110);
            RooRealVar* rrv_sigma0_gaus  = new RooRealVar(("rrv_sigma0_gaus"+label+"_"+channel+spectrum).c_str(),("rrv_sigma1_gaus"+label+"_"+channel+spectrum).c_str(),12,10,32);
            RooRealVar* rrv_mean1_gaus   = new RooRealVar(("rrv_mean1_gaus"+label+"_"+channel+spectrum).c_str(),("rrv_mean1_gaus"+label+"_"+channel+spectrum).c_str(),105,95,130);
	    RooRealVar* rrv_sigma1_gaus  = new RooRealVar(("rrv_sigma1_gaus"+label+"_"+channel+spectrum).c_str(),("rrv_sigma1_gaus"+label+"_"+channel+spectrum).c_str(),26,18.,100);
	  }
	      if (TString(label.c_str()).Contains("_TotalMC_")){
		std::cout<<"For this 500-inf pt bin the model for MC signal pass is  "<<  model << "and tstring is"<< wtagger_label.c_str()    << std::endl;
		RooRealVar* rrv_mean0_gaus   = new RooRealVar(("rrv_mean0_gaus"+label+"_"+channel+spectrum).c_str(),("rrv_mean1_gaus"+label+"_"+channel+spectrum).c_str(),95,93,110);
		RooRealVar* rrv_sigma0_gaus  = new RooRealVar(("rrv_sigma0_gaus"+label+"_"+channel+spectrum).c_str(),("rrv_sigma1_gaus"+label+"_"+channel+spectrum).c_str(),12,7,22);
		RooRealVar* rrv_mean1_gaus   = new RooRealVar(("rrv_mean1_gaus"+label+"_"+channel+spectrum).c_str(),("rrv_mean1_gaus"+label+"_"+channel+spectrum).c_str(),110,93,130);
		RooRealVar* rrv_sigma1_gaus  = new RooRealVar(("rrv_sigma1_gaus"+label+"_"+channel+spectrum).c_str(),("rrv_sigma1_gaus"+label+"_"+channel+spectrum).c_str(),26,25.,100);


	      }
	  */



  
        } // end if signal fail
	      if (TString(label.c_str()).Contains("bkg") and TString(label.c_str()).Contains("fail")){


		RooRealVar* rrv_mean0_gaus   = new RooRealVar(("rrv_mean0_gaus"+label+"_"+channel+spectrum).c_str(),("rrv_mean1_gaus"+label+"_"+channel+spectrum).c_str(),95,93,100);
		RooRealVar* rrv_sigma0_gaus  = new RooRealVar(("rrv_sigma0_gaus"+label+"_"+channel+spectrum).c_str(),("rrv_sigma1_gaus"+label+"_"+channel+spectrum).c_str(),12,7,22);
		RooRealVar* rrv_mean1_gaus   = new RooRealVar(("rrv_mean1_gaus"+label+"_"+channel+spectrum).c_str(),("rrv_mean1_gaus"+label+"_"+channel+spectrum).c_str(),110,95,130);
		RooRealVar* rrv_sigma1_gaus  = new RooRealVar(("rrv_sigma1_gaus"+label+"_"+channel+spectrum).c_str(),("rrv_sigma1_gaus"+label+"_"+channel+spectrum).c_str(),20,12.,100);




	      } // end if bkg fail                                                                                                                                                                                                                                                                                                                                        
              if (TString(label.c_str()).Contains("bkg") and  !TString(label.c_str()).Contains("fail")){


                RooRealVar* rrv_mean0_gaus   = new RooRealVar(("rrv_mean0_gaus"+label+"_"+channel+spectrum).c_str(),("rrv_mean1_gaus"+label+"_"+channel+spectrum).c_str(),95,93,100);
		RooRealVar* rrv_sigma0_gaus  = new RooRealVar(("rrv_sigma0_gaus"+label+"_"+channel+spectrum).c_str(),("rrv_sigma1_gaus"+label+"_"+channel+spectrum).c_str(),12,7,22);
                RooRealVar* rrv_mean1_gaus   = new RooRealVar(("rrv_mean1_gaus"+label+"_"+channel+spectrum).c_str(),("rrv_mean1_gaus"+label+"_"+channel+spectrum).c_str(),110,50,130);
		RooRealVar* rrv_sigma1_gaus  = new RooRealVar(("rrv_sigma1_gaus"+label+"_"+channel+spectrum).c_str(),("rrv_sigma1_gaus"+label+"_"+channel+spectrum).c_str(),20,12.,100);




              } // end if bkg pass  


	      if( (TString(label).Contains("_STop" ) or TString(label).Contains("_W" )  or TString(label).Contains("_QCD" ) ) and !TString(label).Contains("failSubjetTau21cut" )  ) {
		//rrv_c_Exp       = new RooRealVar(("rrv_c_Exp"+label+"_"+channel+spectrum).c_str(),("rrv_c_Exp"+label+"_"+channel+spectrum).c_str(),-0.03,-0.5,0.5);                                                                                                                                                                                                     
		RooRealVar* rrv_mean0_gaus   = new RooRealVar(("rrv_mean0_gaus"+label+"_"+channel+spectrum).c_str(),("rrv_mean1_gaus"+label+"_"+channel+spectrum).c_str(),95,93,100);
		RooRealVar* rrv_sigma0_gaus  = new RooRealVar(("rrv_sigma0_gaus"+label+"_"+channel+spectrum).c_str(),("rrv_sigma1_gaus"+label+"_"+channel+spectrum).c_str(),12,7,22);
		RooRealVar* rrv_mean1_gaus   = new RooRealVar(("rrv_mean1_gaus"+label+"_"+channel+spectrum).c_str(),("rrv_mean1_gaus"+label+"_"+channel+spectrum).c_str(),110,95,130);
		RooRealVar* rrv_sigma1_gaus  = new RooRealVar(("rrv_sigma1_gaus"+label+"_"+channel+spectrum).c_str(),("rrv_sigma1_gaus"+label+"_"+channel+spectrum).c_str(),20,12.,100);




	      }// end if minor bkg


	    } // end if 500-inf          





    


      RooGaussian* gaus0 = new RooGaussian(("gaus0"+label+"_"+channel+spectrum).c_str(),("gaus0"+label+"_"+channel+spectrum).c_str(), *rrv_x,*rrv_mean0_gaus,*rrv_sigma0_gaus);
      RooGaussian* gaus1 = new RooGaussian(("gaus1"+label+"_"+channel+spectrum).c_str(),("gaus1"+label+"_"+channel+spectrum).c_str(), *rrv_x,*rrv_mean1_gaus,*rrv_sigma1_gaus);
      std::cout<< "######## Testing 1,2 ########"<<std::endl;
      RooRealVar* rrv_frac1 = new RooRealVar(("rrv_frac1"+label+"_"+channel+spectrum).c_str(),("rrv_frac1"+label+"_"+channel+spectrum).c_str(),frac_tmp,0,1);
      RooRealVar* rrv_c_Exp       = new RooRealVar(("rrv_c_Exp"+label+"_"+channel+spectrum).c_str(),("rrv_c_Exp"+label+"_"+channel+spectrum).c_str(),-0.05,-0.5,0.5);                                                                                                                                                                                                                                                       
      RooExponential* exp         = new RooExponential(("exp"+label+"_"+channel+spectrum).c_str(),("exp"+label+"_"+channel+spectrum).c_str(),*rrv_x,*rrv_c_Exp);
      std::cout<< "######## Testing 1,2,3. ########"<<std::endl;
      RooAddPdf* model_pdf = new RooAddPdf(("model_pdf"+label+"_"+channel+spectrum).c_str(),("model_pdf"+label+"_"+channel+spectrum).c_str(),RooArgList(*gaus0,*gaus1),RooArgList(*rrv_frac1),1);
      RooAddPdf* model_pdf_dge = new RooAddPdf(("model_pdf_dge"+label+"_"+channel+spectrum).c_str(),("model_pdf_dge"+label+"_"+channel+spectrum).c_str(),RooArgList(*model_pdf,*exp),RooArgList(*rrv_frac1),1);


      return model_pdf_dge ;
    }



    if( model == "ErfExp" ){
      std::cout<< "########### Erf*Exp for mj fit  ############"<<std::endl;
      RooRealVar* rrv_c_ErfExp      = new RooRealVar(("rrv_c_ErfExp"+label+"_"+channel+spectrum).c_str(),("rrv_c_ErfExp"+label+"_"+channel+spectrum).c_str(),-0.026);//,-0.05, 0.05);
      RooRealVar* rrv_offset_ErfExp = new RooRealVar(("rrv_offset_ErfExp"+label+"_"+channel+spectrum).c_str(),("rrv_offset_ErfExp"+label+"_"+channel+spectrum).c_str(),41.,0.,100);
      RooRealVar* rrv_width_ErfExp  = new RooRealVar(("rrv_width_ErfExp"+label+"_"+channel+spectrum).c_str(),("rrv_width_ErfExp"+label+"_"+channel+spectrum).c_str(),30.,1.,100.);
      
      if(!TString(wtagger_label.c_str()).Contains("0v60")){
      if(TString(label).Contains("_WJets0") ) {
        rrv_c_ErfExp      = new RooRealVar(("rrv_c_ErfExp"+label+"_"+channel+spectrum).c_str(),("rrv_c_ErfExp"+label+"_"+channel+spectrum).c_str(),-0.0279,-0.5,0.);
        rrv_offset_ErfExp = new RooRealVar(("rrv_offset_ErfExp"+label+"_"+channel+spectrum).c_str(),("rrv_offset_ErfExp"+label+"_"+channel+spectrum).c_str(),70.,60.,75.);
        rrv_width_ErfExp  = new RooRealVar(("rrv_width_ErfExp"+label+"_"+channel+spectrum).c_str(),("rrv_width_ErfExp"+label+"_"+channel+spectrum).c_str(),23.8,20.,30.);

        if(TString(label).Contains("fail") ) {
          rrv_c_ErfExp      = new RooRealVar(("rrv_c_ErfExp"+label+"_"+channel+spectrum).c_str(),("rrv_c_ErfExp"+label+"_"+channel+spectrum).c_str(),-0.0294,-0.05,0.05);
          rrv_offset_ErfExp = new RooRealVar(("rrv_offset_ErfExp"+label+"_"+channel+spectrum).c_str(),("rrv_offset_ErfExp"+label+"_"+channel+spectrum).c_str(),39.,30.,50.);
          rrv_width_ErfExp  = new RooRealVar(("rrv_width_ErfExp"+label+"_"+channel+spectrum).c_str(),("rrv_width_ErfExp"+label+"_"+channel+spectrum).c_str(),22.5,10.,30.);
        }
        if(TString(wtagger_label.c_str()).Contains("Puppi")){
          
          rrv_c_ErfExp      = new RooRealVar(("rrv_c_ErfExp"+label+"_"+channel+spectrum).c_str(),("rrv_c_ErfExp"+label+"_"+channel+spectrum).c_str(),-0.0279,-0.5,0.);
          rrv_offset_ErfExp = new RooRealVar(("rrv_offset_ErfExp"+label+"_"+channel+spectrum).c_str(),("rrv_offset_ErfExp"+label+"_"+channel+spectrum).c_str(),70.,10.,75.);
          rrv_width_ErfExp  = new RooRealVar(("rrv_width_ErfExp"+label+"_"+channel+spectrum).c_str(),("rrv_width_ErfExp"+label+"_"+channel+spectrum).c_str(),23.8,20.,80.);
        
          if(TString(label).Contains("fail") ) {
            rrv_c_ErfExp      = new RooRealVar(("rrv_c_ErfExp"+label+"_"+channel+spectrum).c_str(),("rrv_c_ErfExp"+label+"_"+channel+spectrum).c_str(),-0.0279,-0.5,0.);
            rrv_offset_ErfExp = new RooRealVar(("rrv_offset_ErfExp"+label+"_"+channel+spectrum).c_str(),("rrv_offset_ErfExp"+label+"_"+channel+spectrum).c_str(),70.,10.,75.);
            rrv_width_ErfExp  = new RooRealVar(("rrv_width_ErfExp"+label+"_"+channel+spectrum).c_str(),("rrv_width_ErfExp"+label+"_"+channel+spectrum).c_str(),23.8,20.,80.);
          }
        }
      }
    }

      RooErfExpPdf* model_pdf       = new RooErfExpPdf(("model_pdf"+label+"_"+channel+spectrum).c_str(),("model_pdf"+label+"_"+channel+spectrum).c_str(),*rrv_x,*rrv_c_ErfExp,*rrv_offset_ErfExp,*rrv_width_ErfExp);
      return model_pdf ;
    }

    if( model == "ExpGaus"){

      RooRealVar* rrv_c_Exp       = new RooRealVar(("rrv_c_Exp"+label+"_"+channel+spectrum).c_str(),("rrv_c_Exp"+label+"_"+channel+spectrum).c_str(),-0.05,-0.5,0.5);
      RooRealVar* rrv_mean1_gaus  = new RooRealVar(("rrv_mean1_gaus"+label+"_"+channel+spectrum).c_str(),("rrv_mean1_gaus"+label+"_"+channel+spectrum).c_str(),84,70,90);
      RooRealVar* rrv_sigma1_gaus = new RooRealVar(("rrv_sigma1_gaus"+label+"_"+channel+spectrum).c_str(),("rrv_sigma1_gaus"+label+"_"+channel+spectrum).c_str(),9.77,7.3,30);
      RooRealVar* rrv_high        = new RooRealVar(("rrv_high"+label+"_"+channel+spectrum).c_str(),("rrv_high"+label+"_"+channel+spectrum).c_str(),0.,0.,1.);
      double sigma1_tmp = 7.77; //6.5932e+00;
      float rangeMean = 4. ;
      float rangeWidth = 5. ;

      if( TString(label).Contains("_STop_failSubjetTau21cut" ) ) {
        rrv_c_Exp       = new RooRealVar(("rrv_c_Exp"+label+"_"+channel+spectrum).c_str(),("rrv_c_Exp"+label+"_"+channel+spectrum).c_str(),-0.03,-0.5,0.5);
        rrv_mean1_gaus  = new RooRealVar(("rrv_mean1_gaus"+label+"_"+channel+spectrum).c_str(),("rrv_mean1_gaus"+label+"_"+channel+spectrum).c_str(),84,60,150);
        //Too narrow limits here often lead to error!! eg max 80
        rrv_sigma1_gaus = new RooRealVar(("rrv_sigma1_gaus"+label+"_"+channel+spectrum).c_str(),("rrv_sigma1_gaus"+label+"_"+channel+spectrum).c_str(),9.33,8.22,60);
        
	  if(TString(wtagger_label.c_str()).Contains("Puppi")){
	   rrv_c_Exp       = new RooRealVar(("rrv_c_Exp"+label+"_"+channel+spectrum).c_str(),("rrv_c_Exp"+label+"_"+channel+spectrum).c_str(),-1.7882e-02,-1.,0.);
	   rrv_mean1_gaus  = new RooRealVar(("rrv_mean1_gaus"+label+"_"+channel+spectrum).c_str(),("rrv_mean1_gaus"+label+"_"+channel+spectrum).c_str(),8.4346e+01 ,75,89); 
	   rrv_sigma1_gaus = new RooRealVar(("rrv_sigma1_gaus"+label+"_"+channel+spectrum).c_str(),("rrv_sigma1_gaus"+label+"_"+channel+spectrum).c_str(),1.1533e+01,5,22);
	   rrv_high        = new RooRealVar(("rrv_high"+label+"_"+channel+spectrum).c_str(),("rrv_high"+label+"_"+channel+spectrum).c_str(),7.3428e-01,0.,1.);
	   }
        
        if(TString(wtagger_label.c_str()).Contains("DDT")){
          rrv_c_Exp       = new RooRealVar(("rrv_c_Exp"+label+"_"+channel+spectrum).c_str(),("rrv_c_Exp"+label+"_"+channel+spectrum).c_str(),8.9813e-03);//,-5.,5.);
          rrv_mean1_gaus  = new RooRealVar(("rrv_mean1_gaus"+label+"_"+channel+spectrum).c_str(),("rrv_mean1_gaus"+label+"_"+channel+spectrum).c_str(),84,75,89); 
          rrv_sigma1_gaus = new RooRealVar(("rrv_sigma1_gaus"+label+"_"+channel+spectrum).c_str(),("rrv_sigma1_gaus"+label+"_"+channel+spectrum).c_str(),7,4,12);
        }
        
      }// end if STop_fail
      if( TString(label).Contains("_QCD") ) {
        rrv_c_Exp       = new RooRealVar(("rrv_c_Exp"+label+"_"+channel+spectrum).c_str(),("rrv_c_Exp"+label+"_"+channel+spectrum).c_str(),-0.005,-0.2,0.2);
        rrv_mean1_gaus  = new RooRealVar(("rrv_mean1_gaus"+label+"_"+channel+spectrum).c_str(),("rrv_mean1_gaus"+label+"_"+channel+spectrum).c_str(),90,0.,150.);
        rrv_sigma1_gaus = new RooRealVar(("rrv_sigma1_gaus"+label+"_"+channel+spectrum).c_str(),("rrv_sigma1_gaus"+label+"_"+channel+spectrum).c_str(),7,4.,50.);
        
        if(TString(wtagger_label.c_str()).Contains("0v60")){
          rrv_c_Exp       = new RooRealVar(("rrv_c_Exp"+label+"_"+channel+spectrum).c_str(),("rrv_c_Exp"+label+"_"+channel+spectrum).c_str(),-1.7882e-02,-1.,0.);
          rrv_mean1_gaus  = new RooRealVar(("rrv_mean1_gaus"+label+"_"+channel+spectrum).c_str(),("rrv_mean1_gaus"+label+"_"+channel+spectrum).c_str(),8.4346e+01 ,75,89); 
          rrv_sigma1_gaus = new RooRealVar(("rrv_sigma1_gaus"+label+"_"+channel+spectrum).c_str(),("rrv_sigma1_gaus"+label+"_"+channel+spectrum).c_str(),1.1533e+01,4,12);
          rrv_high        = new RooRealVar(("rrv_high"+label+"_"+channel+spectrum).c_str(),("rrv_high"+label+"_"+channel+spectrum).c_str(),7.3428e-01,0.,1.);
        }
        
        if(TString(wtagger_label.c_str()).Contains("DDT")){
          rrv_c_Exp       = new RooRealVar(("rrv_c_Exp"+label+"_"+channel+spectrum).c_str(),("rrv_c_Exp"+label+"_"+channel+spectrum).c_str(),-0.05,-0.5,0.5);
          rrv_mean1_gaus  = new RooRealVar(("rrv_mean1_gaus"+label+"_"+channel+spectrum).c_str(),("rrv_mean1_gaus"+label+"_"+channel+spectrum).c_str(),80,70.,95.);
          rrv_sigma1_gaus = new RooRealVar(("rrv_sigma1_gaus"+label+"_"+channel+spectrum).c_str(),("rrv_sigma1_gaus"+label+"_"+channel+spectrum).c_str(),7,4.,12.);   
        }
      }

      if((TString(wtagger_label.c_str()).Contains("300To500") or TString(wtagger_label.c_str()).Contains("200Toinf")  ) and TString(wtagger_label.c_str()).Contains("HP0v55")   ) {
	std::cout<<"For this 300-500 pt bin the model is  "<<  model << "and tstring is"<< wtagger_label.c_str()    << std::endl;
	rrv_sigma1_gaus  = new RooRealVar(("rrv_sigma1_gaus"+label+"_"+channel+spectrum).c_str(),("rrv_sigma1_gaus"+label+"_"+channel+spectrum).c_str(), 16.22 , 15.11, 35. );
      }  
      if(TString(wtagger_label.c_str()).Contains("HP0v40")){

	if(TString(wtagger_label.c_str()).Contains("300To500")){
	  std::cout<<"Model used for 300-500 Medium WP 0.40 is "<<  model << "and tstring containing bkg is "<< wtagger_label.c_str()    << std::endl;
	  rrv_mean1_gaus  = new RooRealVar(("rrv_mean1_gaus"+label+"_"+channel+spectrum).c_str(),("rrv_mean1_gaus"+label+"_"+channel+spectrum).c_str(),84,78.,88.);
	  rrv_sigma1_gaus  = new RooRealVar(("rrv_sigma1_gaus"+label+"_"+channel+spectrum).c_str(),("rrv_sigma1_gaus"+label+"_"+channel+spectrum).c_str(), 14.22 , 13., 30. );
          if( TString(label.c_str()).Contains("bkg") ) {
	    std::cout<<" Model used for 300-500 Medium WP 0.4 for bkg is "<<  model << "and tstring containing bkg is "<< wtagger_label.c_str()    << std::endl;
            rrv_mean1_gaus  = new RooRealVar(("rrv_mean1_gaus"+label+"_"+channel+spectrum).c_str(),("rrv_mean1_gaus"+label+"_"+channel+spectrum).c_str(),84,78.,92.);
            rrv_sigma1_gaus  = new RooRealVar(("rrv_sigma1_gaus"+label+"_"+channel+spectrum).c_str(),("rrv_sigma1_gaus"+label+"_"+channel+spectrum).c_str(), 18. , 15.66 , 50);

          } // end if bkg 300-500
        } 


      } // end Medium WP 0.4 

      if(TString(wtagger_label.c_str()).Contains("HP0v55") ){
      
        if(TString(wtagger_label.c_str()).Contains("200To300")){
	        std::cout<<"For this 200-300 pt bin the model is  "<<  model << "and tstring is"<< wtagger_label.c_str()    << std::endl;
	        rrv_mean1_gaus  = new RooRealVar(("rrv_mean1_gaus"+label+"_"+channel+spectrum).c_str(),("rrv_mean1_gaus"+label+"_"+channel+spectrum).c_str(),54,40.,67.);  
          rrv_sigma1_gaus  = new RooRealVar(("rrv_sigma1_gaus"+label+"_"+channel+spectrum).c_str(),("rrv_sigma1_gaus"+label+"_"+channel+spectrum).c_str(), 25. , 20., 200. );
        }//end if 200-300

        if(TString(wtagger_label.c_str()).Contains("200Toinf") ) {

          if (TString(label.c_str()).Contains("bkg") ){
	          std::cout<<"For this 200-inf pt bin the model is  "<<  model << "and tstring is"<< wtagger_label.c_str()    << std::endl;
            rrv_mean1_gaus  = new RooRealVar(("rrv_mean1_gaus"+label+"_"+channel+spectrum).c_str(),("rrv_mean1_gaus"+label+"_"+channel+spectrum).c_str(),84,76.,90.);
            rrv_sigma1_gaus  = new RooRealVar(("rrv_sigma1_gaus"+label+"_"+channel+spectrum).c_str(),("rrv_sigma1_gaus"+label+"_"+channel+spectrum).c_str(), 16.55 , 14.11, 19. );
            } // end if 200-inf  bkg

          if( !TString(label.c_str()).Contains("bkg") ){
	          std::cout<<"For this 200-inf pt bin the model is  "<<  model << "and tstring is"<< wtagger_label.c_str()    << std::endl;
            rrv_mean1_gaus  = new RooRealVar(("rrv_mean1_gaus"+label+"_"+channel+spectrum).c_str(),("rrv_mean1_gaus"+label+"_"+channel+spectrum).c_str(),86,76.,93.);
            rrv_sigma1_gaus  = new RooRealVar(("rrv_sigma1_gaus"+label+"_"+channel+spectrum).c_str(),("rrv_sigma1_gaus"+label+"_"+channel+spectrum).c_str(), 11. , 6.11, 19.77 );
            } // end if 200-inf and NOT bkg

        } // end if 200-Inf

      } // end if Loose WP


      /* HERWIG
      if(TString(wtagger_label.c_str()).Contains("500Toinf") ) {
	RooRealVar* rrv_c_Exp       = new RooRealVar(("rrv_c_Exp"+label+"_"+channel+spectrum).c_str(),("rrv_c_Exp"+label+"_"+channel+spectrum).c_str(),-0.05,-0.9,0.5);
	if (TString(label.c_str()).Contains("bkg") and !TString(label.c_str()).Contains("fail")){
	  std::cout<<"For this 500-inf pt bin the model forpass bkg is  "<<  model << "and tstring is"<< wtagger_label.c_str()    << std::endl;
	  rrv_mean1_gaus  = new RooRealVar(("rrv_mean1_gaus"+label+"_"+channel+spectrum).c_str(),("rrv_mean1_gaus"+label+"_"+channel+spectrum).c_str(),89,85.,93.);
	  rrv_sigma1_gaus  = new RooRealVar(("rrv_sigma1_gaus"+label+"_"+channel+spectrum).c_str(),("rrv_sigma1_gaus"+label+"_"+channel+spectrum).c_str(), 20.33 , 8.55, 26. );
	} // end if bkg pass                                                                                                                                                                                                                       
	if (!TString(label.c_str()).Contains("bkg") and !TString(label.c_str()).Contains("fail")){
	  std::cout<<"For this 500-inf pt bin the model for signal pass is  "<<  model << "and tstring is"<< wtagger_label.c_str()    << std::endl;
	  rrv_mean1_gaus  = new RooRealVar(("rrv_mean1_gaus"+label+"_"+channel+spectrum).c_str(),("rrv_mean1_gaus"+label+"_"+channel+spectrum).c_str(),89.2,82.,92.);
	  rrv_sigma1_gaus  = new RooRealVar(("rrv_sigma1_gaus"+label+"_"+channel+spectrum).c_str(),("rrv_sigma1_gaus"+label+"_"+channel+spectrum).c_str(), 7.88 , 7.3 , 30. );
	} // end if signal pass                                                                                                                                                                                                                    
	if (!TString(label.c_str()).Contains("bkg") and TString(label.c_str()).Contains("fail")){
	  std::cout<<"For this 500-inf pt bin the model for signal pass is  "<<  model << "and tstring is"<< wtagger_label.c_str()    << std::endl;
	  rrv_mean1_gaus  = new RooRealVar(("rrv_mean1_gaus"+label+"_"+channel+spectrum).c_str(),("rrv_mean1_gaus"+label+"_"+channel+spectrum).c_str(),89,80.,92.);
	  rrv_sigma1_gaus  = new RooRealVar(("rrv_sigma1_gaus"+label+"_"+channel+spectrum).c_str(),("rrv_sigma1_gaus"+label+"_"+channel+spectrum).c_str(), 11.44 , 6.3 , 17. );
	} // end if signal fail                                                                                                                                                                                                                    
	if (TString(label.c_str()).Contains("bkg") and TString(label.c_str()).Contains("fail")){
	  std::cout<<"For this 500-inf pt bin the model for signal pass is  "<<  model << "and tstring is"<< wtagger_label.c_str()    << std::endl;
	  rrv_mean1_gaus  = new RooRealVar(("rrv_mean1_gaus"+label+"_"+channel+spectrum).c_str(),("rrv_mean1_gaus"+label+"_"+channel+spectrum).c_str(),89,81.75,93.);
	  rrv_sigma1_gaus  = new RooRealVar(("rrv_sigma1_gaus"+label+"_"+channel+spectrum).c_str(),("rrv_sigma1_gaus"+label+"_"+channel+spectrum).c_str(), 20.55 , 10.5, 24. );
	} // end if bkg fail                                                                                                                                                                                                                       

	if( TString(label).Contains("_STop" ) and !TString(label).Contains("failSubjetTau21cut" )  ) {
	  //rrv_c_Exp       = new RooRealVar(("rrv_c_Exp"+label+"_"+channel+spectrum).c_str(),("rrv_c_Exp"+label+"_"+channel+spectrum).c_str(),-0.03,-0.5,0.5);                                                                                    
	  rrv_mean1_gaus  = new RooRealVar(("rrv_mean1_gaus"+label+"_"+channel+spectrum).c_str(),("rrv_mean1_gaus"+label+"_"+channel+spectrum).c_str(),91,74,99);
	  rrv_sigma1_gaus = new RooRealVar(("rrv_sigma1_gaus"+label+"_"+channel+spectrum).c_str(),("rrv_sigma1_gaus"+label+"_"+channel+spectrum).c_str(),8.33,4.22,20);
	}


      } // end if 500-inf   

      */


     // OPTIMIZED FOR PYTHIA8 MC
        if(TString(wtagger_label.c_str()).Contains("500Toinf") ) {
	  RooRealVar* rrv_c_Exp       = new RooRealVar(("rrv_c_Exp"+label+"_"+channel+spectrum).c_str(),("rrv_c_Exp"+label+"_"+channel+spectrum).c_str(),-0.05,-2.,0.99);
          if (TString(label.c_str()).Contains("bkg") and !TString(label.c_str()).Contains("fail")){
            std::cout<<"For this 500-inf pt bin the model forpass bkg is  "<<  model << "and tstring is"<< wtagger_label.c_str()    << std::endl;
            rrv_mean1_gaus  = new RooRealVar(("rrv_mean1_gaus"+label+"_"+channel+spectrum).c_str(),("rrv_mean1_gaus"+label+"_"+channel+spectrum).c_str(),89,67.,119.2 );
            rrv_sigma1_gaus  = new RooRealVar(("rrv_sigma1_gaus"+label+"_"+channel+spectrum).c_str(),("rrv_sigma1_gaus"+label+"_"+channel+spectrum).c_str(), 9.33 , 9.55, 16. );
          } // end if bkg pass
          if (!TString(label.c_str()).Contains("bkg") and !TString(label.c_str()).Contains("fail")){
            if (TString(label.c_str()).Contains("_data_")){
            std::cout<<"For this 500-inf pt bin the model for data signal pass is  "<<  model << "and tstring is"<< wtagger_label.c_str()    << std::endl;
            rrv_mean1_gaus  = new RooRealVar(("rrv_mean1_gaus"+label+"_"+channel+spectrum).c_str(),("rrv_mean1_gaus"+label+"_"+channel+spectrum).c_str(),89.2, 67.,119.5 );
            rrv_sigma1_gaus  = new RooRealVar(("rrv_sigma1_gaus"+label+"_"+channel+spectrum).c_str(),("rrv_sigma1_gaus"+label+"_"+channel+spectrum).c_str(), 12.88 , 9.3 , 29. );
            }
	    if (TString(label.c_str()).Contains("_TotalMC_")){
	      std::cout<<"For this 500-inf pt bin the model for MC signal pass is  "<<  model << "and tstring is"<< wtagger_label.c_str()    << std::endl;
	      rrv_mean1_gaus  = new RooRealVar(("rrv_mean1_gaus"+label+"_"+channel+spectrum).c_str(),("rrv_mean1_gaus"+label+"_"+channel+spectrum).c_str(),85.2, 65, 90);//67.,119.9);
	      rrv_sigma1_gaus  = new RooRealVar(("rrv_sigma1_gaus"+label+"_"+channel+spectrum).c_str(),("rrv_sigma1_gaus"+label+"_"+channel+spectrum).c_str(), 11.88 , 5.3 , 12.);// 17); //29. );
            }

           } // end if signal pass
          if (!TString(label.c_str()).Contains("bkg") and TString(label.c_str()).Contains("fail")){
            std::cout<<"For this 500-inf pt bin the model for signal pass is  "<<  model << "and tstring is"<< wtagger_label.c_str()    << std::endl;
            rrv_mean1_gaus  = new RooRealVar(("rrv_mean1_gaus"+label+"_"+channel+spectrum).c_str(),("rrv_mean1_gaus"+label+"_"+channel+spectrum).c_str(),81,67.,90);//109.);
            rrv_sigma1_gaus  = new RooRealVar(("rrv_sigma1_gaus"+label+"_"+channel+spectrum).c_str(),("rrv_sigma1_gaus"+label+"_"+channel+spectrum).c_str(), 11.44 , 8.3 , 17. );
          } // end if signal fail
          if (TString(label.c_str()).Contains("bkg") and TString(label.c_str()).Contains("fail")){
            std::cout<<"For this 500-inf pt bin the model for signal pass is  "<<  model << "and tstring is"<< wtagger_label.c_str()    << std::endl;
            rrv_mean1_gaus  = new RooRealVar(("rrv_mean1_gaus"+label+"_"+channel+spectrum).c_str(),("rrv_mean1_gaus"+label+"_"+channel+spectrum).c_str(),55,45.,60.);
            rrv_sigma1_gaus  = new RooRealVar(("rrv_sigma1_gaus"+label+"_"+channel+spectrum).c_str(),("rrv_sigma1_gaus"+label+"_"+channel+spectrum).c_str(), 35.55 , 25.5, 32. );
          } // end if bkg fail

	  if( (TString(label).Contains("_STop" ) or TString(label).Contains("_W" )  or TString(label).Contains("_QCD" ) )   ) {
	    //rrv_c_Exp       = new RooRealVar(("rrv_c_Exp"+label+"_"+channel+spectrum).c_str(),("rrv_c_Exp"+label+"_"+channel+spectrum).c_str(),-0.03,-0.5,0.5);
	    rrv_mean1_gaus  = new RooRealVar(("rrv_mean1_gaus"+label+"_"+channel+spectrum).c_str(),("rrv_mean1_gaus"+label+"_"+channel+spectrum).c_str(),71,45,60);
	    rrv_sigma1_gaus = new RooRealVar(("rrv_sigma1_gaus"+label+"_"+channel+spectrum).c_str(),("rrv_sigma1_gaus"+label+"_"+channel+spectrum).c_str(),28.33,18.22,55);
          }


        } // end if 500-inf

      

      if( TString(label).Contains("_QCD") ) {
        rrv_c_Exp       = new RooRealVar(("rrv_c_Exp"+label+"_"+channel+spectrum).c_str(),("rrv_c_Exp"+label+"_"+channel+spectrum).c_str(),-0.005,-0.2,0.2);
        rrv_mean1_gaus  = new RooRealVar(("rrv_mean1_gaus"+label+"_"+channel+spectrum).c_str(),("rrv_mean1_gaus"+label+"_"+channel+spectrum).c_str(),90,0.,150.);
        rrv_sigma1_gaus = new RooRealVar(("rrv_sigma1_gaus"+label+"_"+channel+spectrum).c_str(),("rrv_sigma1_gaus"+label+"_"+channel+spectrum).c_str(),11.66,10.,50.);}

      RooExponential* exp         = new RooExponential(("exp"+label+"_"+channel+spectrum).c_str(),("exp"+label+"_"+channel+spectrum).c_str(),*rrv_x,*rrv_c_Exp);
      RooGaussian* gaus           = new RooGaussian(("gaus"+label+"_"+channel+spectrum).c_str(),("gaus"+label+"_"+channel+spectrum).c_str(), *rrv_x,*rrv_mean1_gaus,*rrv_sigma1_gaus);
      RooAddPdf* model_pdf  = new RooAddPdf(("model_pdf"+label+"_"+channel+spectrum).c_str(),("model_pdf"+label+"_"+channel+spectrum).c_str(),RooArgList(*exp,*gaus),RooArgList(*rrv_high));
      return model_pdf ;
    }

    if( model == "ErfExpGaus_sp"){

      RooRealVar* rrv_c_ErfExp    = new RooRealVar(("rrv_c_ErfExp"+label+"_"+channel+spectrum).c_str(),("rrv_c_ErfExp"+label+"_"+channel+spectrum).c_str(),-0.04,-0.2,0.);
      RooRealVar* rrv_width_ErfExp= new RooRealVar(("rrv_width_ErfExp"+label+"_"+channel+spectrum).c_str(),("rrv_width_ErfExp"+label+"_"+channel+spectrum).c_str(),30.,10,150.);
      RooRealVar* rrv_mean1_gaus   = new RooRealVar(("rrv_mean1_gaus"+label+"_"+channel+spectrum).c_str(),("rrv_mean1_gaus"+label+"_"+channel+spectrum).c_str(),80,70,90);
      RooRealVar* rrv_sigma1_gaus  = new RooRealVar(("rrv_sigma1_gaus"+label+"_"+channel+spectrum).c_str(),("rrv_sigma1_gaus"+label+"_"+channel+spectrum).c_str(),20,12,40);
      
      if(TString(wtagger_label.c_str()).Contains("DDT")){
        rrv_c_ErfExp    = new RooRealVar(("rrv_c_ErfExp"+label+"_"+channel+spectrum).c_str(),("rrv_c_ErfExp"+label+"_"+channel+spectrum).c_str(),-4.0352e-02);//,-.,0.);
        rrv_width_ErfExp= new RooRealVar(("rrv_width_ErfExp"+label+"_"+channel+spectrum).c_str(),("rrv_width_ErfExp"+label+"_"+channel+spectrum).c_str(),30.,10,80.);
        rrv_mean1_gaus   = new RooRealVar(("rrv_mean1_gaus"+label+"_"+channel+spectrum).c_str(),("rrv_mean1_gaus"+label+"_"+channel+spectrum).c_str(),80,75,90);
        rrv_sigma1_gaus  = new RooRealVar(("rrv_sigma1_gaus"+label+"_"+channel+spectrum).c_str(),("rrv_sigma1_gaus"+label+"_"+channel+spectrum).c_str(),7,5.,11);
        
        //if( TString(label).Contains("_QCD") ) {
          //rrv_c_ErfExp    = new RooRealVar(("rrv_c_ErfExp"+label+"_"+channel+spectrum).c_str(),("rrv_c_ErfExp"+label+"_"+channel+spectrum).c_str(),-4.0352e-02,-0.09,0.);
	  // rrv_width_ErfExp= new RooRealVar(("rrv_width_ErfExp"+label+"_"+channel+spectrum).c_str(),("rrv_width_ErfExp"+label+"_"+channel+spectrum).c_str(),30.,10,80.);
          //rrv_mean1_gaus   = new RooRealVar(("rrv_mean1_gaus"+label+"_"+channel+spectrum).c_str(),("rrv_mean1_gaus"+label+"_"+channel+spectrum).c_str(),84,75,87);
	  // rrv_sigma1_gaus  = new RooRealVar(("rrv_sigma1_gaus"+label+"_"+channel+spectrum).c_str(),("rrv_sigma1_gaus"+label+"_"+channel+spectrum).c_str(),7,5.,9.);
          
	// }
      }
      

      RooErfExpPdf* erfExp        = new RooErfExpPdf(("erfExp"+label+"_"+channel+spectrum).c_str(),("erfExp"+label+"_"+channel+spectrum).c_str(),*rrv_x,*rrv_c_ErfExp,*rrv_mean1_gaus,*rrv_width_ErfExp);
      RooGaussian* gaus            = new RooGaussian(("gaus"+label+"_"+channel+spectrum).c_str(),("gaus"+label+"_"+channel+spectrum).c_str(), *rrv_x,*rrv_mean1_gaus,*rrv_sigma1_gaus);

      RooRealVar* rrv_high  = new RooRealVar(("rrv_high"+label+"_"+channel+spectrum).c_str(),("rrv_high"+label+"_"+channel+spectrum).c_str(),0.5,0.,1.);
      if( TString(label).Contains("_QCD") )rrv_high  = new RooRealVar(("rrv_high"+label+"_"+channel+spectrum).c_str(),("rrv_high"+label+"_"+channel+spectrum).c_str(),0.8,0.5,1.);
      RooAddPdf* model_pdf  = new RooAddPdf(("model_pdf"+label+"_"+channel+spectrum).c_str(),("model_pdf"+label+"_"+channel+spectrum).c_str(),RooArgList(*erfExp,*gaus),RooArgList(*rrv_high));

      return model_pdf ;
    }

    if( model == "GausErfExp_Wjets"){

      double mean1_tmp = 8.9653e+01;
      double sigma1_tmp = 10.5932e+00;
      float rangeMean = 5. ;
      float rangeWidth = 3. ;
      double frac_tmp = 0.6;
      double c0_tmp     = -3.7180e-02 ;      //double c0_tmp_err     = 6.83e-03;
      double offset_tmp =  8.6888e+01 ;      //double offset_tmp_err = 9.35e+00;
      double width_tmp  =  2.9860e+01 ;      //double width_tmp_err  = 2.97e+00;  
      

      RooRealVar* rrv_mean1_gaus  = new RooRealVar(("rrv_mean1_gaus"+label+"_"+channel+spectrum).c_str(),("rrv_mean1_gaus"+label+"_"+channel+spectrum).c_str(),mean1_tmp, mean1_tmp-rangeMean, mean1_tmp+rangeMean);
      RooRealVar* rrv_sigma1_gaus = new RooRealVar(("rrv_sigma1_gaus"+label+"_"+channel+spectrum).c_str(),("rrv_sigma1_gaus"+label+"_"+channel+spectrum).c_str(),sigma1_tmp, sigma1_tmp-rangeWidth,sigma1_tmp+rangeWidth );
      RooGaussian* gaus1 = new RooGaussian(("gaus1"+label+"_"+channel+spectrum).c_str(),("gaus1"+label+"_"+channel+spectrum).c_str(),*rrv_x,*rrv_mean1_gaus,*rrv_sigma1_gaus);

      RooRealVar* rrv_frac = new RooRealVar(("rrv_frac"+label+"_"+channel+spectrum).c_str(),("rrv_frac"+label+"_"+channel+spectrum).c_str(),frac_tmp,0.4,1);
      RooRealVar* rrv_c_ErfExp      = new RooRealVar(("rrv_c_ErfExp"+label+"_"+channel+spectrum).c_str(),("rrv_c_ErfExp"+label+"_"+channel+spectrum).c_str(),c0_tmp,-10,10.);
      RooRealVar* rrv_offset_ErfExp = new RooRealVar(("rrv_offset_ErfExp"+label+"_"+channel+spectrum).c_str(),("rrv_offset_ErfExp"+label+"_"+channel+spectrum).c_str(),offset_tmp,0.,140.);
      RooRealVar* rrv_width_ErfExp  = new RooRealVar(("rrv_width_ErfExp"+label+"_"+channel+spectrum).c_str(),("rrv_width_ErfExp"+label+"_"+channel+spectrum).c_str(),width_tmp,0.,140.);


      
      RooErfExpPdf* erfExp = new RooErfExpPdf(("erfExp"+label+"_"+channel+spectrum).c_str(),("model_pdf"+label+"_"+channel+spectrum).c_str(),*rrv_x,*rrv_c_ErfExp,*rrv_offset_ErfExp,*rrv_width_ErfExp);
      RooAddPdf* model_pdf = new RooAddPdf(("model_pdf"+label+"_"+channel+spectrum).c_str(),("model_pdf"+label+"_"+channel+spectrum).c_str(),RooArgList(*gaus1,*erfExp),RooArgList(*rrv_frac),1);

      return model_pdf ;
    }

    if( model == "GausErfExp_Wjets_failSubjetTau21cut"){

      double mean1_tmp = 8.9653e+01;
      double sigma1_tmp = 11.5932e+00;
      float rangeMean = 8. ;
      float rangeWidth = 6. ;
      double frac_tmp = 0.6;
      double c0_tmp     = -2.7180e-02 ;      //double c0_tmp_err     = 6.83e-03;
      double offset_tmp =  8.6888e+01 ;      //double offset_tmp_err = 9.35e+00;
      double width_tmp  =  2.9860e+01 ;      //double width_tmp_err  = 2.97e+00;  
      

      RooRealVar* rrv_mean1_gaus  = new RooRealVar(("rrv_mean1_gaus"+label+"_"+channel+spectrum).c_str(),("rrv_mean1_gaus"+label+"_"+channel+spectrum).c_str(),mean1_tmp, mean1_tmp-rangeMean, mean1_tmp+rangeMean);
      RooRealVar* rrv_sigma1_gaus = new RooRealVar(("rrv_sigma1_gaus"+label+"_"+channel+spectrum).c_str(),("rrv_sigma1_gaus"+label+"_"+channel+spectrum).c_str(),sigma1_tmp, sigma1_tmp-rangeWidth,sigma1_tmp+rangeWidth );
      RooGaussian* gaus1 = new RooGaussian(("gaus1"+label+"_"+channel+spectrum).c_str(),("gaus1"+label+"_"+channel+spectrum).c_str(),*rrv_x,*rrv_mean1_gaus,*rrv_sigma1_gaus);

      RooRealVar* rrv_frac = new RooRealVar(("rrv_frac"+label+"_"+channel+spectrum).c_str(),("rrv_frac"+label+"_"+channel+spectrum).c_str(),frac_tmp,0.4,1);
      RooRealVar* rrv_c_ErfExp      = new RooRealVar(("rrv_c_ErfExp"+label+"_"+channel+spectrum).c_str(),("rrv_c_ErfExp"+label+"_"+channel+spectrum).c_str(),c0_tmp,-10,10.);
      RooRealVar* rrv_offset_ErfExp = new RooRealVar(("rrv_offset_ErfExp"+label+"_"+channel+spectrum).c_str(),("rrv_offset_ErfExp"+label+"_"+channel+spectrum).c_str(),offset_tmp,0.,140.);
      RooRealVar* rrv_width_ErfExp  = new RooRealVar(("rrv_width_ErfExp"+label+"_"+channel+spectrum).c_str(),("rrv_width_ErfExp"+label+"_"+channel+spectrum).c_str(),width_tmp,0.,140.);


      
      RooErfExpPdf* erfExp = new RooErfExpPdf(("erfExp"+label+"_"+channel+spectrum).c_str(),("model_pdf"+label+"_"+channel+spectrum).c_str(),*rrv_x,*rrv_c_ErfExp,*rrv_offset_ErfExp,*rrv_width_ErfExp);
      RooAddPdf* model_pdf = new RooAddPdf(("model_pdf"+label+"_"+channel+spectrum).c_str(),("model_pdf"+label+"_"+channel+spectrum).c_str(),RooArgList(*gaus1,*erfExp),RooArgList(*rrv_frac),1);

      return model_pdf ;
    }

    if( model == "GausErfExp_QCD"){

      double mean1_tmp = 8.7653e+01;
      double sigma1_tmp = 7.5932e+00;
      float rangeMean = 6. ;
      float rangeWidth = 6. ;
      double frac_tmp = 0.6;
      double c0_tmp     = -2.7180e-02 ;      //double c0_tmp_err     = 6.83e-03;
      double offset_tmp =  8.6888e+01 ;      //double offset_tmp_err = 9.35e+00;
      double width_tmp  =  2.9860e+01 ;      //double width_tmp_err  = 2.97e+00;  
      

      RooRealVar* rrv_mean1_gaus  = new RooRealVar(("rrv_mean1_gaus"+label+"_"+channel+spectrum).c_str(),("rrv_mean1_gaus"+label+"_"+channel+spectrum).c_str(),mean1_tmp, mean1_tmp-rangeMean, mean1_tmp+rangeMean);
      RooRealVar* rrv_sigma1_gaus = new RooRealVar(("rrv_sigma1_gaus"+label+"_"+channel+spectrum).c_str(),("rrv_sigma1_gaus"+label+"_"+channel+spectrum).c_str(),sigma1_tmp, sigma1_tmp-rangeWidth,sigma1_tmp+rangeWidth );
      RooGaussian* gaus1 = new RooGaussian(("gaus1"+label+"_"+channel+spectrum).c_str(),("gaus1"+label+"_"+channel+spectrum).c_str(),*rrv_x,*rrv_mean1_gaus,*rrv_sigma1_gaus);

      RooRealVar* rrv_frac = new RooRealVar(("rrv_frac"+label+"_"+channel+spectrum).c_str(),("rrv_frac"+label+"_"+channel+spectrum).c_str(),frac_tmp,0.4,1);
      RooRealVar* rrv_c_ErfExp      = new RooRealVar(("rrv_c_ErfExp"+label+"_"+channel+spectrum).c_str(),("rrv_c_ErfExp"+label+"_"+channel+spectrum).c_str(),c0_tmp,-10,10.);
      RooRealVar* rrv_offset_ErfExp = new RooRealVar(("rrv_offset_ErfExp"+label+"_"+channel+spectrum).c_str(),("rrv_offset_ErfExp"+label+"_"+channel+spectrum).c_str(),offset_tmp,0.,140.);
      RooRealVar* rrv_width_ErfExp  = new RooRealVar(("rrv_width_ErfExp"+label+"_"+channel+spectrum).c_str(),("rrv_width_ErfExp"+label+"_"+channel+spectrum).c_str(),width_tmp,0.,140.);


      
      RooErfExpPdf* erfExp = new RooErfExpPdf(("erfExp"+label+"_"+channel+spectrum).c_str(),("model_pdf"+label+"_"+channel+spectrum).c_str(),*rrv_x,*rrv_c_ErfExp,*rrv_offset_ErfExp,*rrv_width_ErfExp);
      RooAddPdf* model_pdf = new RooAddPdf(("model_pdf"+label+"_"+channel+spectrum).c_str(),("model_pdf"+label+"_"+channel+spectrum).c_str(),RooArgList(*gaus1,*erfExp),RooArgList(*rrv_frac),1);

      return model_pdf ;
    }

    if( model == "DeuxGausChebychev"){

      RooAbsPdf* model_pdf = NULL ;
      RooAbsPdf* model_pdf_dgc = NULL ;

      //double p0_tmp = 3.1099e-01 ; double p0_tmp_err = 5.e-01; //1.86e-01;
      //double p1_tmp = -2.2128e-01; double p1_tmp_err = 5.02e-01; //3.02e-01;
      // double frac_tmp =  4.6400e-01  ; double frac_tmp_err =  5.02e-01; //1.20e-01;
      //double mean1_tmp = 8.7682e+01;
      //double sigma1_tmp = 12.;

      double p0_tmp = 4.1099e-01 ; double p0_tmp_err = 5.e-01; //1.86e-01;                                                                                                                                         
      double p1_tmp = -2.2128e-01; double p1_tmp_err = 5.02e-01; //3.02e-01;                                                                                                                                       
      double frac_tmp =  5.6400e-01  ; double frac_tmp_err =  2.02e-01; //1.20e-01;                                                                                                                                
      double mean1_tmp = 62.;  //8.9682e+01;
      double mean1_low = 55.;
      double mean1_high = 65.;
      double sigma1_tmp = 12.; //12.; I CHANGED THESE 2 variables
      double sigma1_low = 11.; 
      double sigma1_high = 19.;

      double mean2_tmp = 80.; 
 //8.9682e+01;                                                                                                                                                                        
      double sigma2_tmp = 19.; //12.; I ADDED THIS SECOND GAUSSIAN                                                                                                                                                
 
      double mean2_low = 75.;
      double mean2_high = 92.;
      double sigma2_high = 20.;

      std::cout<<"Model used is ********  "<<  model << "and tstring is"<< wtagger_label.c_str()    << std::endl;

      if(TString(wtagger_label.c_str()).Contains("500Toinf")){
	std::cout<<"For this 500-Inf pt bin the model is  "<<  model << "and tstring is"<< wtagger_label.c_str()    << std::endl;
	double mean2_tmp = 85.; 
        double mean2_low = 80.;
        double mean2_high = 87.; 
	double sigma2_tmp = 9.;
        double sigma2_high = 15.44;
      }

      if(TString(wtagger_label.c_str()).Contains("300To500")  and TString(wtagger_label.c_str()).Contains("HP0v40")  ){
	std::cout<<"For this 300-500 pt bin in the Medium WP the model is  "<<  model << "and tstring is"<< wtagger_label.c_str()    << std::endl;
	mean1_tmp = 50.;
	mean1_low = 49.; 
	mean1_high = 51.;
	sigma1_tmp = 27.; 
	sigma1_low = 26.;
	sigma1_high = 39.;
	
        //p0_tmp = 4.5099e-01 ;
	frac_tmp = 0.35; // 0.4;  // 5.6400e-01  ; 

        mean2_tmp = 86.;
        mean2_low = 80.;
        mean2_high = 89.;
        sigma2_tmp = 9.;
        sigma2_high = 25.;
      }

      if(TString(wtagger_label.c_str()).Contains("200ToInf")  and TString(wtagger_label.c_str()).Contains("HP0v40")  ){
	std::cout<<"For this 200-inf pt bin in the Medium WP the model is  "<<  model << "and tstring is"<< wtagger_label.c_str()    << std::endl;
        mean1_tmp = 50.;
        mean1_low = 49.;
        mean1_high = 51.;
        sigma1_tmp = 27.;
        sigma1_low = 26.;
        sigma1_high = 39.;

        //p0_tmp = 4.5099e-01 ;                                                                                                                                                                                                                       
        frac_tmp = 0.37; // 0.4;  // 5.6400e-01  ;                                                                                                                                                                                                    

        mean2_tmp = 86.;
        mean2_low = 80.;
        mean2_high = 89.;
        sigma2_tmp = 9.;
        sigma2_high = 25.;
      }


      RooRealVar* rrv_mean1_gaus = new RooRealVar(("rrv_mean1_gaus"+label+"_"+channel+spectrum).c_str(),("rrv_mean1_gaus"+label+"_"+channel+spectrum).c_str(),mean1_tmp, mean1_low, mean1_high);
      RooRealVar* rrv_sigma1_gaus = new RooRealVar(("rrv_sigma1_gaus"+label+"_"+channel+spectrum).c_str(),("rrv_sigma1_gaus"+label+"_"+channel+spectrum).c_str(),sigma1_tmp, sigma1_low, sigma1_high );
      RooGaussian* gaus1 = new RooGaussian(("gaus1"+label+"_"+channel+spectrum).c_str(),("gaus1"+label+"_"+channel+spectrum).c_str(),*rrv_x,*rrv_mean1_gaus,*rrv_sigma1_gaus);

      RooRealVar* rrv_mean2_gaus = new RooRealVar(("rrv_mean2_gaus"+label+"_"+channel+spectrum).c_str(),("rrv_mean2_gaus"+label+"_"+channel+spectrum).c_str(),mean2_tmp, mean2_low , mean2_high );
      RooRealVar* rrv_sigma2_gaus = new RooRealVar(("rrv_sigma2_gaus"+label+"_"+channel+spectrum).c_str(),("rrv_sigma2_gaus"+label+"_"+channel+spectrum).c_str(),sigma2_tmp,8., sigma2_high );
      RooGaussian* gaus2 = new RooGaussian(("gaus2"+label+"_"+channel+spectrum).c_str(),("gaus2"+label+"_"+channel+spectrum).c_str(),*rrv_x,*rrv_mean2_gaus,*rrv_sigma2_gaus);

      RooRealVar* rrv_p0_cheb = new RooRealVar(("rrv_p0_cheb"+label+"_"+channel+spectrum).c_str(),("rrv_p0_cheb"+label+"_"+channel+spectrum).c_str(),p0_tmp);
      RooRealVar* rrv_p1_cheb = new RooRealVar(("rrv_p1_cheb"+label+"_"+channel+spectrum).c_str(),("rrv_p1_cheb"+label+"_"+channel+spectrum).c_str(),p1_tmp);

      RooChebychev* chebbb = new RooChebychev(("chebbb"+label+"_"+channel+spectrum).c_str(),("chebbb"+label+"_"+channel+spectrum).c_str(), *rrv_x, RooArgList(*rrv_p0_cheb,*rrv_p1_cheb) );

      RooRealVar* rrv_frac = new RooRealVar(("rrv_frac"+label+"_"+channel+spectrum).c_str(),("rrv_frac"+label+"_"+channel+spectrum).c_str(),frac_tmp);
     
      model_pdf = new RooAddPdf(("model_pdf"+label+"_"+channel+spectrum).c_str(),("model_pdf"+label+"_"+channel+spectrum).c_str(),RooArgList(*gaus1,*gaus2),RooArgList(*rrv_frac),1);
      model_pdf_dgc = new RooAddPdf(("model_pdf_dgc"+label+"_"+channel+spectrum).c_str(),("model_pdf_dgc"+label+"_"+channel+spectrum).c_str(),RooArgList(*model_pdf, *chebbb),RooArgList(*rrv_frac),1);

      return model_pdf_dgc ;
    }
    
    if( model == "GausErfExp_QCD_failSubjetTau21cut"){

      double mean1_tmp = 60. ; //8.7653e+01;
      double sigma1_tmp = 11.; //7.5932e+00;
      float rangeMean = 6. ;
      float rangeWidth = 10. ;
      double frac_tmp = 0.6;
      double c0_tmp     = -2.7180e-02 ;      //double c0_tmp_err     = 6.83e-03;
      double offset_tmp =  8.6888e+01 ;      //double offset_tmp_err = 9.35e+00;
      double width_tmp  =  2.9860e+01 ;      //double width_tmp_err  = 2.97e+00;  
      

      RooRealVar* rrv_mean1_gaus  = new RooRealVar(("rrv_mean1_gaus"+label+"_"+channel+spectrum).c_str(),("rrv_mean1_gaus"+label+"_"+channel+spectrum).c_str(),mean1_tmp, mean1_tmp-rangeMean, mean1_tmp+rangeMean);
      RooRealVar* rrv_sigma1_gaus = new RooRealVar(("rrv_sigma1_gaus"+label+"_"+channel+spectrum).c_str(),("rrv_sigma1_gaus"+label+"_"+channel+spectrum).c_str(),sigma1_tmp, sigma1_tmp-rangeWidth,sigma1_tmp+rangeWidth );
      RooGaussian* gaus1 = new RooGaussian(("gaus1"+label+"_"+channel+spectrum).c_str(),("gaus1"+label+"_"+channel+spectrum).c_str(),*rrv_x,*rrv_mean1_gaus,*rrv_sigma1_gaus);

      RooRealVar* rrv_frac = new RooRealVar(("rrv_frac"+label+"_"+channel+spectrum).c_str(),("rrv_frac"+label+"_"+channel+spectrum).c_str(),frac_tmp,0.4,1);
      RooRealVar* rrv_c_ErfExp      = new RooRealVar(("rrv_c_ErfExp"+label+"_"+channel+spectrum).c_str(),("rrv_c_ErfExp"+label+"_"+channel+spectrum).c_str(),c0_tmp,-10,10.);
      RooRealVar* rrv_offset_ErfExp = new RooRealVar(("rrv_offset_ErfExp"+label+"_"+channel+spectrum).c_str(),("rrv_offset_ErfExp"+label+"_"+channel+spectrum).c_str(),offset_tmp,0.,140.);
      RooRealVar* rrv_width_ErfExp  = new RooRealVar(("rrv_width_ErfExp"+label+"_"+channel+spectrum).c_str(),("rrv_width_ErfExp"+label+"_"+channel+spectrum).c_str(),width_tmp,0.,140.);


      
      RooErfExpPdf* erfExp = new RooErfExpPdf(("erfExp"+label+"_"+channel+spectrum).c_str(),("model_pdf"+label+"_"+channel+spectrum).c_str(),*rrv_x,*rrv_c_ErfExp,*rrv_offset_ErfExp,*rrv_width_ErfExp);
      RooAddPdf* model_pdf = new RooAddPdf(("model_pdf"+label+"_"+channel+spectrum).c_str(),("model_pdf"+label+"_"+channel+spectrum).c_str(),RooArgList(*gaus1,*erfExp),RooArgList(*rrv_frac),1);

      return model_pdf ;
    }
    

    if( model == "GausErfExp_ttbar"){

      double mean1_tmp = 8.4653e+01;
      double sigma1_tmp = 7.5932e+00;
      float rangeMean = 6. ;
      float rangeWidth = 5. ;
      double frac_tmp = 1.0;
      double c0_tmp     = -2.7180e-02 ;      //double c0_tmp_err     = 6.83e-03;
      double offset_tmp =  8.6888e+01 ;      //double offset_tmp_err = 9.35e+00;
      double width_tmp  =  2.9860e+01 ;      //double width_tmp_err  = 2.97e+00;  
      
      std::cout<<"Model used is "<<  model << "and tstring is"<< wtagger_label.c_str()    << std::endl;
     
      if(TString(wtagger_label.c_str()).Contains("0v60")){
        mean1_tmp = 8.2402e+01;   
        sigma1_tmp = 7.5645e+00;            
        rangeMean = 6. ;
        rangeWidth = 5. ;
        c0_tmp     = -4.2672e-02 ;
        offset_tmp =  8.5656e+01 ;
        width_tmp  =  2.5308e+01  ;
      }
      if( TString(wtagger_label.c_str()).Contains("PuppiSD") ){
        mean1_tmp = 83.;  //8.0857e+01;
        sigma1_tmp = 12.4035e+00;
        rangeMean = 2. ;
        rangeWidth = 10. ;
        c0_tmp     = -2.1046e-02  ;
        offset_tmp =  8.0122e+01 ;
        width_tmp  =  2.9595e+01 ;
          
        if(TString(wtagger_label.c_str()).Contains("0v56")){
          mean1_tmp = 8.2402e+01;
          sigma1_tmp = 7.5645e+00;
          rangeMean = 6. ;
          rangeWidth = 5. ;
          c0_tmp     = -4.2672e-02 ;
          offset_tmp =  8.5656e+01 ;
          width_tmp  =  2.5308e+01  ;
        }
      }
      
      if(TString(wtagger_label.c_str()).Contains("DDT")){
        
        if(TString(wtagger_label.c_str()).Contains("0v38")){
          mean1_tmp = 8.6000e+01;
          sigma1_tmp = 7.2154e+00;
          c0_tmp     = -1.7193e-01 ;
          offset_tmp =  1.1819e+02 ;
          width_tmp  =   2.3273e+01  ;
        }
        
        if(TString(wtagger_label.c_str()).Contains("0v52")){
          mean1_tmp = 86.;   
          sigma1_tmp = 1.0008e+01 ;            
          rangeMean = 6. ;
          rangeWidth = 5. ;
          c0_tmp     = -1.7193e-01 ;
          offset_tmp =  1.1819e+02 ;
          width_tmp  =  2.3273e+01  ;
        }
        if(TString(wtagger_label.c_str()).Contains("0v44")){
          mean1_tmp = 8.6138e+01 ;   
          sigma1_tmp = 9.9019e+00 ;            
          rangeMean = 6. ;
          rangeWidth = 5. ;
          c0_tmp     = -1.2532e-01 ;
          offset_tmp =  1.1819e+02  ;
          width_tmp  =  2.3299e+00  ;
          // frac_tmp = 9.9757e-01
        }
      }

      RooRealVar* rrv_mean1_gaus  = new RooRealVar(("rrv_mean1_gaus"+label+"_"+channel+spectrum).c_str(),("rrv_mean1_gaus"+label+"_"+channel+spectrum).c_str(),mean1_tmp, mean1_tmp-rangeMean, mean1_tmp+rangeMean);
      RooRealVar* rrv_sigma1_gaus = new RooRealVar(("rrv_sigma1_gaus"+label+"_"+channel+spectrum).c_str(),("rrv_sigma1_gaus"+label+"_"+channel+spectrum).c_str(),sigma1_tmp, sigma1_tmp-rangeWidth,sigma1_tmp+rangeWidth );
      RooGaussian* gaus1 = new RooGaussian(("gaus1"+label+"_"+channel+spectrum).c_str(),("gaus1"+label+"_"+channel+spectrum).c_str(),*rrv_x,*rrv_mean1_gaus,*rrv_sigma1_gaus);

      float offset_tmp_err = 20;;
      
      RooRealVar* rrv_c_ErfExp      = new RooRealVar(("rrv_c_ErfExp"+label+"_"+channel+spectrum).c_str(),("rrv_c_ErfExp"+label+"_"+channel+spectrum).c_str(),c0_tmp,c0_tmp-4e-2, c0_tmp+4e-2 );
      RooRealVar* rrv_offset_ErfExp = new RooRealVar(("rrv_offset_ErfExp"+label+"_"+channel+spectrum).c_str(),("rrv_offset_ErfExp"+label+"_"+channel+spectrum).c_str(),offset_tmp,offset_tmp-offset_tmp_err*4,offset_tmp+offset_tmp_err*4);
      RooRealVar* rrv_width_ErfExp  = new RooRealVar(("rrv_width_ErfExp"+label+"_"+channel+spectrum).c_str(),("rrv_width_ErfExp"+label+"_"+channel+spectrum).c_str(),width_tmp, width_tmp-10, width_tmp+10);
      
     
      RooRealVar* rrv_frac = new RooRealVar(("rrv_frac"+label+"_"+channel+spectrum).c_str(),("rrv_frac"+label+"_"+channel+spectrum).c_str(),frac_tmp);
      

      rrv_c_ErfExp     ->setConstant(kTRUE);
      rrv_offset_ErfExp->setConstant(kTRUE);
      rrv_width_ErfExp ->setConstant(kTRUE);
      
      RooErfExpPdf* erfExp = new RooErfExpPdf(("erfExp"+label+"_"+channel+spectrum).c_str(),("model_pdf"+label+"_"+channel+spectrum).c_str(),*rrv_x,*rrv_c_ErfExp,*rrv_offset_ErfExp,*rrv_width_ErfExp);
      RooAddPdf* model_pdf = new RooAddPdf(("model_pdf"+label+"_"+channel+spectrum).c_str(),("model_pdf"+label+"_"+channel+spectrum).c_str(),RooArgList(*gaus1,*erfExp),RooArgList(*rrv_frac),1);

      return model_pdf ;
    }

    if( model == "Gaus_ttbar"){

      double mean1_tmp = 80.5;
      double sigma1_tmp = 10.1149e+00;
      float rangeMean = 5. ;
      float rangeWidth = 10;

      RooRealVar* rrv_mean1_gaus  = new RooRealVar(("rrv_mean1_gaus"+label+"_"+channel+spectrum).c_str(),("rrv_mean1_gaus"+label+"_"+channel+spectrum).c_str(),mean1_tmp, mean1_tmp-4, mean1_tmp+9);
      RooRealVar* rrv_sigma1_gaus = new RooRealVar(("rrv_sigma1_gaus"+label+"_"+channel+spectrum).c_str(),("rrv_sigma1_gaus"+label+"_"+channel+spectrum).c_str(),sigma1_tmp, 7, 20);// was 10

      if( TString(label.c_str()).Contains("bkg") ) rrv_sigma1_gaus  = new RooRealVar(("rrv_sigma1_gaus"+label+"_"+channel+spectrum).c_str(),("rrv_sigma1_gaus"+label+"_"+channel+spectrum).c_str(),sigma1_tmp+3, sigma1_tmp-rangeWidth+3,sigma1_tmp+rangeWidth +3);

      if( TString(label.c_str()).Contains("fail") ){
        if( TString(label).Contains("data") ) {
          rrv_mean1_gaus  = workspace->var(("rrv_mean1_gaus_ttbar_data_"+channel+spectrum).c_str());
          rrv_sigma1_gaus = workspace->var(("rrv_sigma1_gaus_ttbar_data_"+channel+spectrum).c_str());
        }
        else if( TString(label).Contains("TotalMC") ) {
          rrv_mean1_gaus  = workspace->var(("rrv_mean1_gaus_ttbar_TotalMC_"+channel+spectrum).c_str());
          rrv_sigma1_gaus = workspace->var(("rrv_sigma1_gaus_ttbar_TotalMC_"+channel+spectrum).c_str());
        }
      }

      RooGaussian* gaus1 = new RooGaussian(("gaus1"+label+"_"+channel+spectrum).c_str(),("gaus1"+label+"_"+channel+spectrum).c_str(),*rrv_x,*rrv_mean1_gaus,*rrv_sigma1_gaus);

      return gaus1 ;
    }

    if( model == "Gaus"){

      std::cout << "Making Gaus1" << std::endl;
      RooRealVar* rrv_mean1_gaus   = new RooRealVar(("rrv_mean1_gaus"+label+"_"+channel+spectrum).c_str(),("rrv_mean1_gaus"+label+"_"+channel+spectrum).c_str(),80,75,100);
      RooRealVar* rrv_sigma1_gaus  = new RooRealVar(("rrv_sigma1_gaus"+label+"_"+channel+spectrum).c_str(),("rrv_sigma1_gaus"+label+"_"+channel+spectrum).c_str(),7,0.,15);  
      RooGaussian* model_pdf       = new RooGaussian(("gaus"+label+"_"+channel+spectrum).c_str(),("gaus"+label+"_"+channel+spectrum).c_str(), *rrv_x,*rrv_mean1_gaus,*rrv_sigma1_gaus);
      std::cout << "Done" << std::endl;
      return model_pdf ;
    }


    if( model == "GausChebychev_ttbar_failSubjetTau21cut"){

      RooAbsPdf* model_pdf = NULL ;

      double p0_tmp = 3.1099e-01 ; double p0_tmp_err = 1.86e-01;
      double p1_tmp = -2.2128e-01; double p1_tmp_err = 3.02e-01;
      double frac_tmp =  4.6400e-01  ; double frac_tmp_err = 1.20e-01;
      double mean1_tmp = 88.;
      double mean1_low = 84.;     // double mean1_high = 92.;
      double mean1_high = 92.;  
      double sigma1_tmp = 9.2789e+00;
      double sigma1_low = 5.;
      double sigma1_high = 25.;

      if(TString(wtagger_label.c_str()).Contains("500Toinf")){
        //#p0_tmp = 2.1208e-01 ;
        //#p1_tmp = -3.2198e-01;
        //#frac_tmp = 4.3714e-01;
	mean1_tmp = 90.;
	mean1_low = 84.;
	mean1_high = 92.;
	sigma1_tmp = 15.77;
	sigma1_low = 10.;
	sigma1_high = 25.;
      }
      
      if(TString(wtagger_label.c_str()).Contains("DDT")){
        if(TString(wtagger_label.c_str()).Contains("0v38")){
        p0_tmp = 3.7004e-01 ;
        p1_tmp = -4.5610e-01;
        frac_tmp = 6.8410e-01;
        mean1_tmp = 8.7682e+01;
        sigma1_tmp = 9.2789e+00;
      }
      }

      // take the same gaussian used in the pass sample
      RooAbsPdf* gaus = NULL ;
      //if( TString(label).Contains("data"   ) ) gaus = workspace->pdf(("gaus1_ttbar_data_"+channel+spectrum).c_str());
      //if( TString(label).Contains("TotalMC") ) gaus = workspace->pdf(("gaus1_ttbar_TotalMC_"+channel+spectrum).c_str());
      //if( TString(label).Contains("realW")   ) gaus = workspace->pdf(("gaus1_TTbar_realW_"+channel+spectrum).c_str());

      RooRealVar* rrv_mean1_gaus = new RooRealVar(("rrv_mean1_gaus"+label+"_"+channel+spectrum).c_str(),("rrv_mean1_gaus"+label+"_"+channel+spectrum).c_str(),mean1_tmp, mean1_low, mean1_high);
      RooRealVar* rrv_sigma1_gaus = new RooRealVar(("rrv_sigma1_gaus"+label+"_"+channel+spectrum).c_str(),("rrv_sigma1_gaus"+label+"_"+channel+spectrum).c_str(),sigma1_tmp, sigma1_low, sigma1_high );
      gaus = new RooGaussian(("gaus"+label+"_"+channel+spectrum).c_str(),("gaus1"+label+"_"+channel+spectrum).c_str(),*rrv_x,*rrv_mean1_gaus,*rrv_sigma1_gaus);

      RooRealVar* rrv_p0_cheb = new RooRealVar(("rrv_p0_cheb"+label+"_"+channel+spectrum).c_str(),("rrv_p0_cheb"+label+"_"+channel+spectrum).c_str(),p0_tmp);
      RooRealVar* rrv_p1_cheb = new RooRealVar(("rrv_p1_cheb"+label+"_"+channel+spectrum).c_str(),("rrv_p1_cheb"+label+"_"+channel+spectrum).c_str(),p1_tmp);

      RooChebychev* cheb = new RooChebychev(("cheb"+label+"_"+channel+spectrum).c_str(),("cheb"+label+"_"+channel+spectrum).c_str(), *rrv_x, RooArgList(*rrv_p0_cheb,*rrv_p1_cheb) );

      RooRealVar* rrv_frac = new RooRealVar(("rrv_frac"+label+"_"+channel+spectrum).c_str(),("rrv_frac"+label+"_"+channel+spectrum).c_str(),frac_tmp);
      model_pdf = new RooAddPdf(("model_pdf"+label+"_"+channel+spectrum).c_str(),("model_pdf"+label+"_"+channel+spectrum).c_str(),RooArgList(*gaus,*cheb),RooArgList(*rrv_frac),1);

      return model_pdf ;
    }

    if( model == "GausChebychev_ttbar"){

      RooAbsPdf* model_pdf = NULL ;

      double p0_tmp = 3.1099e-01 ; double p0_tmp_err = 1.86e-01;
      double p1_tmp = -2.2128e-01; double p1_tmp_err = 3.02e-01;
      double frac_tmp =  4.6400e-01  ; double frac_tmp_err = 1.20e-01;
      double mean1_tmp = 8.7682e+01;
      double sigma1_tmp = 11.2789e+00;
      double sigma1_low = 5.;
      double sigma1_high = 12.;

      double mean1_low = 84.;     // double mean1_high = 92.;                                                                                                                                                                                                 
      double mean1_high = 92.;

      if(TString(wtagger_label.c_str()).Contains("500Toinf")){
        mean1_tmp = 83.;
        mean1_low = 82.;
        mean1_high = 87.;
      }

      if(TString(wtagger_label.c_str()).Contains("300To500")){
        sigma1_tmp = 14.;
        sigma1_low = 10.;
        sigma1_high = 25.;
       
      }

      // take the same gaussian used in the pass sample
      //RooAbsPdf* gaus = NULL ;
      //if( TString(label).Contains("data"   ) ) gaus = workspace->pdf(("gaus1_ttbar_data_"+channel+spectrum).c_str());
      //if( TString(label).Contains("TotalMC") ) gaus = workspace->pdf(("gaus1_ttbar_TotalMC_"+channel+spectrum).c_str());
      //if( TString(label).Contains("realW")   ) gaus = workspace->pdf(("gaus1_TTbar_realW_"+channel+spectrum).c_str());
      RooRealVar* rrv_mean1_gaus = new RooRealVar(("rrv_mean1_gaus"+label+"_"+channel+spectrum).c_str(),("rrv_mean1_gaus"+label+"_"+channel+spectrum).c_str(),mean1_tmp, mean1_low, mean1_high);
      RooRealVar* rrv_sigma1_gaus = new RooRealVar(("rrv_sigma1_gaus"+label+"_"+channel+spectrum).c_str(),("rrv_sigma1_gaus"+label+"_"+channel+spectrum).c_str(),sigma1_tmp, sigma1_low, sigma1_high );
      RooGaussian* gaus = new RooGaussian(("gaus"+label+"_"+channel+spectrum).c_str(),("gaus1"+label+"_"+channel+spectrum).c_str(),*rrv_x,*rrv_mean1_gaus,*rrv_sigma1_gaus);


      RooRealVar* rrv_p0_cheb2 = new RooRealVar(("rrv_p0_cheb2"+label+"_"+channel+spectrum).c_str(),("rrv_p0_cheb2"+label+"_"+channel+spectrum).c_str(),p0_tmp);
      RooRealVar* rrv_p1_cheb2 = new RooRealVar(("rrv_p1_cheb2"+label+"_"+channel+spectrum).c_str(),("rrv_p1_cheb2"+label+"_"+channel+spectrum).c_str(),p1_tmp);

      RooChebychev* cheb2 = new RooChebychev(("cheb2"+label+"_"+channel+spectrum).c_str(),("cheb2"+label+"_"+channel+spectrum).c_str(), *rrv_x, RooArgList(*rrv_p0_cheb2,*rrv_p1_cheb2) );

      RooRealVar* rrv_frac = new RooRealVar(("rrv_frac"+label+"_"+channel+spectrum).c_str(),("rrv_frac"+label+"_"+channel+spectrum).c_str(),frac_tmp);
      model_pdf = new RooAddPdf(("model_pdf"+label+"_"+channel+spectrum).c_str(),("model_pdf"+label+"_"+channel+spectrum).c_str(),RooArgList(*gaus,*cheb2),RooArgList(*rrv_frac),1);

      return model_pdf ;
    }


    if( model == "GausErfExp_ttbar_failSubjetTau21cut"){

      double c0_tmp     = -3.0626e-02 ;      double c0_tmp_err = 1.46e-02;
      double offset_tmp = 5.1636e+01  ;      double offset_tmp_err = 4.92e+01;
      double width_tmp  = 5.6186e+01  ;      double width_tmp_err = 4.69e+00;
      double frac_tmp   = 1.          ;
      double mean1_tmp  = 8.0486e+01;
      double sigma1_tmp = 7.7456e+00;
      
      RooAbsPdf* model_pdf = NULL ;
      
   
      // take the same gaussian used in the pass sample
      RooAbsPdf* gaus = NULL ;
      if( TString(label).Contains("data"   ) ) gaus = workspace->pdf(("gaus1_ttbar_data_"+channel+spectrum).c_str());
      if( TString(label).Contains("TotalMC") ) gaus = workspace->pdf(("gaus1_ttbar_TotalMC_"+channel+spectrum).c_str());
      
      // RooRealVar* rrv_mean1_gaus = new RooRealVar(("rrv_mean1_gaus"+label+"_"+channel+spectrum).c_str(),("rrv_mean1_gaus"+label+"_"+channel+spectrum).c_str(),mean1_tmp, 75., 90.);
      //      if( TString(label).Contains("data"   ) ) rrv_mean1_gaus = workspace->var( ("rrv_mean1_gaus_ttbar_data_"+channel+spectrum).c_str() );
      //     if( TString(label).Contains("TotalMC") ) rrv_mean1_gaus = workspace->var( ("rrv_mean1_gaus_ttbar_TotalMC_"+channel+spectrum).c_str() );
      //     RooRealVar* rrv_sigma1_gaus = new RooRealVar(("rrv_sigma1_gaus"+label+"_"+channel+spectrum).c_str(),("rrv_sigma1_gaus"+label+"_"+channel+spectrum).c_str(),sigma1_tmp,0.,sigma1_tmp+10 );
      //     RooGaussian* gaus = new RooGaussian(("gaus"+label+"_"+channel+spectrum).c_str(),("gaus1"+label+"_"+channel+spectrum).c_str(),*rrv_x,*rrv_mean1_gaus,*rrv_sigma1_gaus);

      RooRealVar* rrv_c_ErfExp = new RooRealVar(("rrv_c_ErfExp"+label+"_"+channel+spectrum).c_str(),("rrv_c_ErfExp"+label+"_"+channel+spectrum).c_str(),c0_tmp,c0_tmp-4e-2, c0_tmp+4e-2);
      RooRealVar* rrv_offset_ErfExp = new RooRealVar(("rrv_offset_ErfExp"+label+"_"+channel+spectrum).c_str(),("rrv_offset_ErfExp"+label+"_"+channel+spectrum).c_str(),offset_tmp,offset_tmp-offset_tmp_err,offset_tmp+offset_tmp_err);
      RooRealVar* rrv_width_ErfExp = new RooRealVar(("rrv_width_ErfExp"+label+"_"+channel+spectrum).c_str(),("rrv_width_ErfExp"+label+"_"+channel+spectrum).c_str(), width_tmp,width_tmp-width_tmp_err, width_tmp+width_tmp_err);

      RooErfExpPdf* erfExp = new RooErfExpPdf(("erfExp"+label+"_"+channel+spectrum).c_str(),("model_pdf"+label+"_"+channel+spectrum).c_str(),*rrv_x,*rrv_c_ErfExp,*rrv_offset_ErfExp,*rrv_width_ErfExp);

      RooRealVar* rrv_frac = new RooRealVar(("rrv_frac"+label+"_"+channel+spectrum).c_str(),("rrv_frac"+label+"_"+channel+spectrum).c_str(),frac_tmp);
      
      rrv_c_ErfExp     ->setConstant(kTRUE);
      rrv_offset_ErfExp->setConstant(kTRUE);
      rrv_width_ErfExp ->setConstant(kTRUE);
      
      model_pdf = new RooAddPdf(("model_pdf"+label+"_"+channel+spectrum).c_str(),("model_pdf"+label+"_"+channel+spectrum).c_str(),RooArgList(*gaus,*erfExp),RooArgList(*rrv_frac),1);

      return model_pdf ;
    }

    if( model == "ErfExp_ttbar"){

      double c0_tmp     = -2.7180e-02 ;      double c0_tmp_err     = 0.1 ; //6.83e-03;
      double offset_tmp =  8.6888e+01 ;      double offset_tmp_err = 11.; //9.35e+00;
      double width_tmp  =  2.9860e+01 ;      double width_tmp_err  = 5. ; //2.97e+00;

      if(TString(wtagger_label.c_str()).Contains("76X")){
        c0_tmp     = -1.9681e-02 ;
        offset_tmp =  7.4564e+01 ;
        width_tmp  =  2.6397e+01 ;
      }
      if(TString(wtagger_label.c_str()).Contains("0v60")){
        c0_tmp     = -2.9373e-02 ;  
        offset_tmp =  8.2980e+01 ;
        width_tmp  =  3.6133e+01 ;
        if(TString(wtagger_label.c_str()).Contains("76X")){
          c0_tmp     = -2.2689e-02 ;
          offset_tmp =  6.9803e+01 ;
          width_tmp  =  3.2077e+01 ;
        }
      }
      
      if( TString(wtagger_label.c_str()).Contains("PuppiSD") ){
        c0_tmp     =  -2.7046e-02 ; // PARAMETERS 1 erfexp_ttbar puppi SD     
        offset_tmp =   8.2122e+01 ;// was 8.2122e+01      
        width_tmp  =  5. ; // was 2.9595e+01
      }
      
      
      if(TString(wtagger_label.c_str()).Contains("DDT")){
        if(TString(wtagger_label.c_str()).Contains("0v38")){
          c0_tmp     = -6.0079e-02  ;
          offset_tmp =  1.4980e+02 ;
          width_tmp  =  4.8168e+01  ;
        }
        if(TString(wtagger_label.c_str()).Contains("0v52")){
          c0_tmp     =     -3.1793e-02  ;
          offset_tmp =  9.7997e+01 ;
          width_tmp  =  3.8820e+01  ;
        }
        if(TString(wtagger_label.c_str()).Contains("0v44")){
          c0_tmp     = -4.1927e-02 ;
          offset_tmp =  1.1240e+02  ;
          width_tmp  =  3.9190e+01  ;
        }
      }
        
        
      RooRealVar* rrv_c_ErfExp      = new RooRealVar(("rrv_c_ErfExp"+label+"_"+channel+spectrum).c_str(),("rrv_c_ErfExp"+label+"_"+channel+spectrum).c_str(),c0_tmp,c0_tmp-4e-2, c0_tmp+4e-2 );
      RooRealVar* rrv_offset_ErfExp = new RooRealVar(("rrv_offset_ErfExp"+label+"_"+channel+spectrum).c_str(),("rrv_offset_ErfExp"+label+"_"+channel+spectrum).c_str(),offset_tmp,offset_tmp-offset_tmp_err*4,offset_tmp+offset_tmp_err*4);
      RooRealVar* rrv_width_ErfExp  = new RooRealVar(("rrv_width_ErfExp"+label+"_"+channel+spectrum).c_str(),("rrv_width_ErfExp"+label+"_"+channel+spectrum).c_str(),width_tmp, width_tmp-10, width_tmp+10);
      

      RooErfExpPdf* model_pdf = new RooErfExpPdf(("model_pdf"+label+"_"+channel+spectrum).c_str(),("model_pdf"+label+"_"+channel+spectrum).c_str(),*rrv_x,*rrv_c_ErfExp,*rrv_offset_ErfExp,*rrv_width_ErfExp);

      RooGaussian* gaus1 = addConstraint(rrv_c_ErfExp,rrv_c_ErfExp->getVal(),c0_tmp_err,constraint);
      RooGaussian* gaus2 = addConstraint(rrv_offset_ErfExp,rrv_offset_ErfExp->getVal(),offset_tmp_err,constraint);
      RooGaussian* gaus3 = addConstraint(rrv_width_ErfExp,rrv_width_ErfExp->getVal(),width_tmp_err,constraint);
      workspace->import(*gaus1);
      workspace->import(*gaus2);
      workspace->import(*gaus3);
      return model_pdf ;
    }

    if( model == "ErfExp_ttbar_failSubjetTau21cut"){

      RooErfExpPdf* model_pdf = NULL ;

      double c0_tmp = -3.0626e-02    ;      double c0_tmp_err = 1.46e-02;
      double offset_tmp = 5.1636e+01 ;      double offset_tmp_err = 4.92e+01;
      double width_tmp = 3.6186e+01  ;      double width_tmp_err = 4.69e+00;

      if(TString(wtagger_label.c_str()).Contains("76X")){
        c0_tmp = -2.8654e-02    ;
        offset_tmp = 4.5140e+01 ;
        width_tmp = 3.4083e+01  ;
      }
      if(TString(wtagger_label.c_str()).Contains("0v60")){
        c0_tmp = -3.4131e-02    ;  
        offset_tmp = 3.3961e+01 ;
        width_tmp = 3.2876e+01  ;
        if(TString(wtagger_label.c_str()).Contains("76X")){
          c0_tmp = -3.3221e-02    ; 
          offset_tmp = 2.9445e+01 ;
          width_tmp = 2.5680e+01  ;
        }
      }
      if( TString(wtagger_label.c_str()).Contains("PuppiSD") ){     
        c0_tmp = -3.160e-02    ;       c0_tmp_err = 1.46e-02; // PARAMETERS 2 
        offset_tmp = 6.5935e+01 ;       offset_tmp_err = 4.92e+01;
        width_tmp = 3.9583e+01  ;       width_tmp_err = 4.69e+00;
      }
      
      if(TString(wtagger_label.c_str()).Contains("DDT")){
        if(TString(wtagger_label.c_str()).Contains("0v38")){
          c0_tmp     = -5.9405e-02 ;
          offset_tmp =  1.4790e+02 ;
          width_tmp  =  5.3544e+01  ;
        }
        if(TString(wtagger_label.c_str()).Contains("0v52")){
          c0_tmp     = -4.0722e-02  ;
          offset_tmp =  1.0108e+02 ;
          width_tmp  =  4.9796e+01  ;
        }
        if(TString(wtagger_label.c_str()).Contains("0v44")){
          c0_tmp     = -2.0670e-02 ;
          offset_tmp =  6.1299e+01  ;
          width_tmp  =  3.0247e+01  ;
          
        }
      }
         

      RooRealVar* rrv_c_ErfExp = new RooRealVar(("rrv_c_ErfExp"+label+"_"+channel+spectrum).c_str(),("rrv_c_ErfExp"+label+"_"+channel+spectrum).c_str(),c0_tmp,c0_tmp-4e-2, c0_tmp+4e-2);
      RooRealVar* rrv_offset_ErfExp = new RooRealVar(("rrv_offset_ErfExp"+label+"_"+channel+spectrum).c_str(),("rrv_offset_ErfExp"+label+"_"+channel+spectrum).c_str(),offset_tmp);
      RooRealVar* rrv_width_ErfExp = new RooRealVar(("rrv_width_ErfExp"+label+"_"+channel+spectrum).c_str(),("rrv_width_ErfExp"+label+"_"+channel+spectrum).c_str(), width_tmp);
      
      model_pdf = new RooErfExpPdf(("model_pdf"+label+"_"+channel+spectrum).c_str(),("model_pdf"+label+"_"+channel+spectrum).c_str(),*rrv_x,*rrv_c_ErfExp,*rrv_offset_ErfExp,*rrv_width_ErfExp);
      RooGaussian* gaus1 = addConstraint(rrv_c_ErfExp,rrv_c_ErfExp->getVal(),c0_tmp_err,constraint);
      workspace->import(*gaus1);
      return model_pdf ;
    }
  }


  // FOR MC FITS TO MATCHED TT MC!!!    
  else if( TString(label).Contains("realW") or TString(label).Contains("fakeW")){

    if(model == "CB"){
      std::cout<< "########### Cystal Ball for mj fit ############"<<std::endl;
      RooRealVar* rrv_mean_CB  = new RooRealVar(("rrv_mean_CB"+label+"_"+channel+spectrum).c_str(),("rrv_mean_CB"+label+"_"+channel+spectrum).c_str(),84,78,88);
      RooRealVar* rrv_sigma_CB = new RooRealVar(("rrv_sigma_CB"+label+"_"+channel+spectrum).c_str(),("rrv_sigma_CB"+label+"_"+channel+spectrum).c_str(),7,4,10);
      RooRealVar* rrv_alpha_CB = new RooRealVar(("rrv_alpha_CB"+label+"_"+channel+spectrum).c_str(),("rrv_alpha_CB"+label+"_"+channel+spectrum).c_str(),-2,-4,-0.5);
      RooRealVar* rrv_n_CB     = new RooRealVar(("rrv_n_CB"+label+"_"+channel+spectrum).c_str(),("rrv_n_CB"+label+"_"+channel+spectrum).c_str(),2,0.,4);
      RooCBShape* model_pdf = new RooCBShape(("model_pdf"+label+"_"+channel+spectrum).c_str(),("model_pdf"+label+"_"+channel+spectrum).c_str(), *rrv_x,*rrv_mean_CB,*rrv_sigma_CB,*rrv_alpha_CB,*rrv_n_CB);


      return model_pdf ;
    }

    if( model == "DeuxGaus"){
      double frac_tmp = 0.3;

      std::cout << "Making gaus0" << std::endl;
      std::cout<<"For this 500-inf pt bin the model for MC Matched ttbar signal pass is "<<  model << "and tstring is"<< wtagger_label.c_str()    << std::endl;
      //      RooRealVar* rrv_mean0_gaus   = new RooRealVar(("rrv_mean0_gaus"+label+"_"+channel+spectrum).c_str(),("rrv_mean1_gaus"+label+"_"+channel+spectrum).c_str(),91,81,90);
      // RooRealVar* rrv_sigma0_gaus  = new RooRealVar(("rrv_sigma0_gaus"+label+"_"+channel+spectrum).c_str(),("rrv_sigma1_gaus"+label+"_"+channel+spectrum).c_str(),12,7,13);//22);
      // RooRealVar* rrv_mean1_gaus   = new RooRealVar(("rrv_mean1_gaus"+label+"_"+channel+spectrum).c_str(),("rrv_mean1_gaus"+label+"_"+channel+spectrum).c_str(),110,90,130);
      // RooRealVar* rrv_sigma1_gaus  = new RooRealVar(("rrv_sigma1_gaus"+label+"_"+channel+spectrum).c_str(),("rrv_sigma1_gaus"+label+"_"+channel+spectrum).c_str(),26,20.,45. );//100);

      RooRealVar* rrv_mean0_gaus   = new RooRealVar(("rrv_mean0_gaus"+label+"_"+channel+spectrum).c_str(),("rrv_mean1_gaus"+label+"_"+channel+spectrum).c_str(),81,71,87);
      RooRealVar* rrv_sigma0_gaus  = new RooRealVar(("rrv_sigma0_gaus"+label+"_"+channel+spectrum).c_str(),("rrv_sigma1_gaus"+label+"_"+channel+spectrum).c_str(),8,7,9);//13);                              
      RooRealVar* rrv_mean1_gaus   = new RooRealVar(("rrv_mean1_gaus"+label+"_"+channel+spectrum).c_str(),("rrv_mean1_gaus"+label+"_"+channel+spectrum).c_str(),110,90,130);
      RooRealVar* rrv_sigma1_gaus  = new RooRealVar(("rrv_sigma1_gaus"+label+"_"+channel+spectrum).c_str(),("rrv_sigma1_gaus"+label+"_"+channel+spectrum).c_str(),26,15.,45. );//100);                      



      RooGaussian* gaus0 = new RooGaussian(("gaus0"+label+"_"+channel+spectrum).c_str(),("gaus0"+label+"_"+channel+spectrum).c_str(), *rrv_x,*rrv_mean0_gaus,*rrv_sigma0_gaus);
      RooGaussian* gaus1 = new RooGaussian(("gaus1"+label+"_"+channel+spectrum).c_str(),("gaus1"+label+"_"+channel+spectrum).c_str(), *rrv_x,*rrv_mean1_gaus,*rrv_sigma1_gaus);                                   

      std::cout<< "######## Testing 1,2 ########"<<std::endl;                                                                                                                                                     

      RooRealVar* rrv_frac1 = new RooRealVar(("rrv_frac1"+label+"_"+channel+spectrum).c_str(),("rrv_frac1"+label+"_"+channel+spectrum).c_str(),frac_tmp,0,1);

      std::cout<< "######## Testing 1,2,3. ########"<<std::endl;
      RooAddPdf* model_pdf = new RooAddPdf(("model_pdf"+label+"_"+channel+spectrum).c_str(),("model_pdf"+label+"_"+channel+spectrum).c_str(),RooArgList(*gaus0,*gaus1),RooArgList(*rrv_frac1),1);                 



      return model_pdf ;
    }


    if( model == "Gaus_SigFail"){

      std::cout << "Making gaus for signal fail" << std::endl;
      RooRealVar* rrv_mean1a_gaus   = new RooRealVar(("rrv_mean1a_gaus"+label+"_"+channel+spectrum).c_str(),("rrv_mean1a_gaus"+label+"_"+channel+spectrum).c_str(),80,70,100);
      RooRealVar* rrv_sigma1a_gaus  = new RooRealVar(("rrv_sigma1a_gaus"+label+"_"+channel+spectrum).c_str(),("rrv_sigma1a_gaus"+label+"_"+channel+spectrum).c_str(),5.33 ,0.,12);
      RooGaussian* model_pdf       = new RooGaussian(("gaus"+label+"_"+channel+spectrum).c_str(),("gaus"+label+"_"+channel+spectrum).c_str(), *rrv_x,*rrv_mean1a_gaus,*rrv_sigma1a_gaus);
      std::cout << "Done" << std::endl;
      return model_pdf ;
    }

    if( model == "Gaus_Sig"){

      std::cout << "Making gaus for signal fail" << std::endl;
      RooRealVar* rrv_mean1ap_gaus   = new RooRealVar(("rrv_mean1ap_gaus"+label+"_"+channel+spectrum).c_str(),("rrv_mean1ap_gaus"+label+"_"+channel+spectrum).c_str(),90,70,100);
      RooRealVar* rrv_sigma1ap_gaus  = new RooRealVar(("rrv_sigma1ap_gaus"+label+"_"+channel+spectrum).c_str(),("rrv_sigma1ap_gaus"+label+"_"+channel+spectrum).c_str(),12.33 ,7.,16);
      RooGaussian* model_pdf       = new RooGaussian(("gaus"+label+"_"+channel+spectrum).c_str(),("gaus"+label+"_"+channel+spectrum).c_str(), *rrv_x,*rrv_mean1ap_gaus,*rrv_sigma1ap_gaus);
      std::cout << "Done" << std::endl;
      return model_pdf ;
    }

    if( model == "Gaus_QCD"){

      std::cout << "Making gaus" << std::endl;
      RooRealVar* rrv_mean1_gaus   = new RooRealVar(("rrv_mean1_gaus"+label+"_"+channel+spectrum).c_str(),("rrv_mean1_gaus"+label+"_"+channel+spectrum).c_str(),57,45,65);
      RooRealVar* rrv_sigma1_gaus  = new RooRealVar(("rrv_sigma1_gaus"+label+"_"+channel+spectrum).c_str(),("rrv_sigma1_gaus"+label+"_"+channel+spectrum).c_str(),22.33 ,14.,23);
      RooGaussian* model_pdf       = new RooGaussian(("gaus"+label+"_"+channel+spectrum).c_str(),("gaus"+label+"_"+channel+spectrum).c_str(), *rrv_x,*rrv_mean1_gaus,*rrv_sigma1_gaus);
      std::cout << "Done" << std::endl;
      return model_pdf ;
    }

    if( model == "Poly5"){
      std::cout << "Making 5th order Polynomial" << std::endl;
      RooRealVar* rrv_polyCo1 = new RooRealVar(("rrv_polyCo1"+label+"_"+channel+spectrum).c_str(),("rrv_polyCo1"+label+"_"+channel+spectrum).c_str(),0., -10., 10.);
      RooRealVar* rrv_polyCo2 = new RooRealVar(("rrv_polyCo2"+label+"_"+channel+spectrum).c_str(),("rrv_polyCo2"+label+"_"+channel+spectrum).c_str(),0., -10., 10.);
      RooRealVar* rrv_polyCo3 = new RooRealVar(("rrv_polyCo3"+label+"_"+channel+spectrum).c_str(),("rrv_polyCo3"+label+"_"+channel+spectrum).c_str(),0., -10., 10.);
      RooRealVar* rrv_polyCo4 = new RooRealVar(("rrv_polyCo4"+label+"_"+channel+spectrum).c_str(),("rrv_polyCo4"+label+"_"+channel+spectrum).c_str(),0., -10., 10.);
      RooRealVar* rrv_polyCo5 = new RooRealVar(("rrv_polyCo5"+label+"_"+channel+spectrum).c_str(),("rrv_polyCo5"+label+"_"+channel+spectrum).c_str(),0., -10., 10.);

      RooPolynomial* model_pdf = new RooPolynomial(("model_pdf"+label+"_"+channel+spectrum).c_str(),("model_pdf"+label+"_"+channel+spectrum).c_str(),*rrv_x, RooArgList(*rrv_polyCo1, *rrv_polyCo2, *rrv_polyCo3, *rrv_polyCo4 , *rrv_polyCo5 ));
      std::cout << "Done" << std::endl;
      return model_pdf ;
    }


    if( model == "Exp"){
      std::cout << "Making Exp2" << std::endl;
      std::cout<< "######### Exp = levelled exp funtion for W+jets mlvj ############" <<std::endl;
      RooRealVar* rrv_c_Exp = new RooRealVar(("rrv_c_Exp"+label+"_"+channel+spectrum).c_str(),("rrv_c_Exp"+label+"_"+channel+spectrum).c_str(),-0.030, -0.2, 0.05);
      RooExponential* model_pdf = new RooExponential(("model_pdf"+label+"_"+channel+spectrum).c_str(),("model_pdf"+label+"_"+channel+spectrum).c_str(),*rrv_x,*rrv_c_Exp);
      std::cout << "Done" << std::endl;
      return model_pdf ;
    }

    if( model == "ErfExp" ){
      std::cout<< "########### Erf*Exp for mj fit  ############"<<std::endl;
      RooRealVar* rrv_c_ErfExp      = new RooRealVar(("rrv_c_ErfExp"+label+"_"+channel+spectrum).c_str(),("rrv_c_ErfExp"+label+"_"+channel+spectrum).c_str(),-0.026);//,-0.05, 0.05);
      RooRealVar* rrv_offset_ErfExp = new RooRealVar(("rrv_offset_ErfExp"+label+"_"+channel+spectrum).c_str(),("rrv_offset_ErfExp"+label+"_"+channel+spectrum).c_str(),81.,10.,140);
      RooRealVar* rrv_width_ErfExp  = new RooRealVar(("rrv_width_ErfExp"+label+"_"+channel+spectrum).c_str(),("rrv_width_ErfExp"+label+"_"+channel+spectrum).c_str(),80.,10.,140.);

      if(TString(label).Contains("_WJets0") ) {
        rrv_c_ErfExp      = new RooRealVar(("rrv_c_ErfExp"+label+"_"+channel+spectrum).c_str(),("rrv_c_ErfExp"+label+"_"+channel+spectrum).c_str(),-0.0279,-0.5,0.);
        rrv_offset_ErfExp = new RooRealVar(("rrv_offset_ErfExp"+label+"_"+channel+spectrum).c_str(),("rrv_offset_ErfExp"+label+"_"+channel+spectrum).c_str(),70.,10.,150.);
        rrv_width_ErfExp  = new RooRealVar(("rrv_width_ErfExp"+label+"_"+channel+spectrum).c_str(),("rrv_width_ErfExp"+label+"_"+channel+spectrum).c_str(),23.8,20.,30.);

        if(TString(label).Contains("fail") ) {
          rrv_c_ErfExp      = new RooRealVar(("rrv_c_ErfExp"+label+"_"+channel+spectrum).c_str(),("rrv_c_ErfExp"+label+"_"+channel+spectrum).c_str(),-0.0294,-0.05,0.05);
          rrv_offset_ErfExp = new RooRealVar(("rrv_offset_ErfExp"+label+"_"+channel+spectrum).c_str(),("rrv_offset_ErfExp"+label+"_"+channel+spectrum).c_str(),39.,30.,50.);
          rrv_width_ErfExp  = new RooRealVar(("rrv_width_ErfExp"+label+"_"+channel+spectrum).c_str(),("rrv_width_ErfExp"+label+"_"+channel+spectrum).c_str(),22.5,10.,30.);
        }
      }

      RooErfExpPdf* model_pdf       = new RooErfExpPdf(("model_pdf"+label+"_"+channel+spectrum).c_str(),("model_pdf"+label+"_"+channel+spectrum).c_str(),*rrv_x,*rrv_c_ErfExp,*rrv_offset_ErfExp,*rrv_width_ErfExp);
      return model_pdf ;
    }

    if( model == "ExpGaus"){

      RooRealVar* rrv_c_Exp       = new RooRealVar(("rrv_c_Exp"+label+"_"+channel+spectrum).c_str(),("rrv_c_Exp"+label+"_"+channel+spectrum).c_str(),-0.05,-0.5,0.5);
      RooRealVar* rrv_mean1_gaus  = new RooRealVar(("rrv_mean1_gaus"+label+"_"+channel+spectrum).c_str(),("rrv_mean1_gaus"+label+"_"+channel+spectrum).c_str(),84,70,90);
      RooRealVar* rrv_sigma1_gaus = new RooRealVar(("rrv_sigma1_gaus"+label+"_"+channel+spectrum).c_str(),("rrv_sigma1_gaus"+label+"_"+channel+spectrum).c_str(),7,4,40);
      RooRealVar* rrv_high        = new RooRealVar(("rrv_high"+label+"_"+channel+spectrum).c_str(),("rrv_high"+label+"_"+channel+spectrum).c_str(),0.,0.,1.);

      //if( TString(label.c_str()).Contains("bkg") ) rrv_sigma1_gaus  = new RooRealVar(("rrv_sigma1_gaus"+label+"_"+channel+spectrum).c_str(),("rrv_sigma1_gaus"+label+"_"+channel+spectrum).c_str(),sigma1_tmp+3, sigma1_tmp-rangeWidth+3,sigma1_tmp+rangeWidth +3);

      if( TString(label).Contains("_STop_failSubjetTau21cut" ) ) {
        rrv_c_Exp       = new RooRealVar(("rrv_c_Exp"+label+"_"+channel+spectrum).c_str(),("rrv_c_Exp"+label+"_"+channel+spectrum).c_str(),-0.03,-0.5,0.5);
        rrv_mean1_gaus  = new RooRealVar(("rrv_mean1_gaus"+label+"_"+channel+spectrum).c_str(),("rrv_mean1_gaus"+label+"_"+channel+spectrum).c_str(),84,60,150); //Too narrow limits here often lead to error!! eg max 80
        rrv_sigma1_gaus = new RooRealVar(("rrv_sigma1_gaus"+label+"_"+channel+spectrum).c_str(),("rrv_sigma1_gaus"+label+"_"+channel+spectrum).c_str(),7,4,60);
      }
      if( TString(label).Contains("_QCD") ) {
        rrv_c_Exp       = new RooRealVar(("rrv_c_Exp"+label+"_"+channel+spectrum).c_str(),("rrv_c_Exp"+label+"_"+channel+spectrum).c_str(),-0.005,-0.2,0.2);
        rrv_mean1_gaus  = new RooRealVar(("rrv_mean1_gaus"+label+"_"+channel+spectrum).c_str(),("rrv_mean1_gaus"+label+"_"+channel+spectrum).c_str(),90,0.,150.);
        rrv_sigma1_gaus = new RooRealVar(("rrv_sigma1_gaus"+label+"_"+channel+spectrum).c_str(),("rrv_sigma1_gaus"+label+"_"+channel+spectrum).c_str(),7,4.,50.);
      }
      RooExponential* exp         = new RooExponential(("exp"+label+"_"+channel+spectrum).c_str(),("exp"+label+"_"+channel+spectrum).c_str(),*rrv_x,*rrv_c_Exp);
      RooGaussian* gaus           = new RooGaussian(("gaus"+label+"_"+channel+spectrum).c_str(),("gaus"+label+"_"+channel+spectrum).c_str(), *rrv_x,*rrv_mean1_gaus,*rrv_sigma1_gaus);
      RooAddPdf* model_pdf  = new RooAddPdf(("model_pdf"+label+"_"+channel+spectrum).c_str(),("model_pdf"+label+"_"+channel+spectrum).c_str(),RooArgList(*exp,*gaus),RooArgList(*rrv_high));
      return model_pdf ;
    }

    if( model == "Gaus_ttbar"){

      double mean1_tmp = 80.5;
      double sigma1_tmp = 10.1149e+00;
      float rangeMean = 5. ;
      float rangeWidth = 10;

      RooRealVar* rrv_mean1_gaus  = new RooRealVar(("rrv_mean1_gaus"+label+"_"+channel+spectrum).c_str(),("rrv_mean1_gaus"+label+"_"+channel+spectrum).c_str(),mean1_tmp, mean1_tmp-4, mean1_tmp+9);
      RooRealVar* rrv_sigma1_gaus = new RooRealVar(("rrv_sigma1_gaus"+label+"_"+channel+spectrum).c_str(),("rrv_sigma1_gaus"+label+"_"+channel+spectrum).c_str(),sigma1_tmp, 7, 20);// was 10

      if( TString(label.c_str()).Contains("bkg") ) rrv_sigma1_gaus  = new RooRealVar(("rrv_sigma1_gaus"+label+"_"+channel+spectrum).c_str(),("rrv_sigma1_gaus"+label+"_"+channel+spectrum).c_str(),sigma1_tmp+3, sigma1_tmp-rangeWidth+3,sigma1_tmp+rangeWidth +3);

      if( TString(label.c_str()).Contains("fail") ){
        if( TString(label).Contains("data") ) {
          rrv_mean1_gaus  = workspace->var(("rrv_mean1_gaus_ttbar_data_"+channel+spectrum).c_str());
          rrv_sigma1_gaus = workspace->var(("rrv_sigma1_gaus_ttbar_data_"+channel+spectrum).c_str());
        }
        else if( TString(label).Contains("TotalMC") ) {
          rrv_mean1_gaus  = workspace->var(("rrv_mean1_gaus_ttbar_TotalMC_"+channel+spectrum).c_str());
          rrv_sigma1_gaus = workspace->var(("rrv_sigma1_gaus_ttbar_TotalMC_"+channel+spectrum).c_str());
        }
      }

      RooGaussian* gaus1 = new RooGaussian(("gaus1"+label+"_"+channel+spectrum).c_str(),("gaus1"+label+"_"+channel+spectrum).c_str(),*rrv_x,*rrv_mean1_gaus,*rrv_sigma1_gaus);

      return gaus1 ;
    }


    if( model == "ErfExpGaus_sp"){

      RooRealVar* rrv_c_ErfExp    = new RooRealVar(("rrv_c_ErfExp"+label+"_"+channel+spectrum).c_str(),("rrv_c_ErfExp"+label+"_"+channel+spectrum).c_str(),-0.04,-0.2,0.);
      RooRealVar* rrv_width_ErfExp= new RooRealVar(("rrv_width_ErfExp"+label+"_"+channel+spectrum).c_str(),("rrv_width_ErfExp"+label+"_"+channel+spectrum).c_str(),30.,10,150.);
      RooRealVar* rrv_mean1_gaus   = new RooRealVar(("rrv_mean1_gaus"+label+"_"+channel+spectrum).c_str(),("rrv_mean1_gaus"+label+"_"+channel+spectrum).c_str(),80,60,90);
      RooRealVar* rrv_sigma1_gaus  = new RooRealVar(("rrv_sigma1_gaus"+label+"_"+channel+spectrum).c_str(),("rrv_sigma1_gaus"+label+"_"+channel+spectrum).c_str(),7,0.,40);

      RooErfExpPdf* erfExp        = new RooErfExpPdf(("erfExp"+label+"_"+channel+spectrum).c_str(),("erfExp"+label+"_"+channel+spectrum).c_str(),*rrv_x,*rrv_c_ErfExp,*rrv_mean1_gaus,*rrv_width_ErfExp);
      RooGaussian* gaus            = new RooGaussian(("gaus"+label+"_"+channel+spectrum).c_str(),("gaus"+label+"_"+channel+spectrum).c_str(), *rrv_x,*rrv_mean1_gaus,*rrv_sigma1_gaus);

      RooRealVar* rrv_high  = new RooRealVar(("rrv_high"+label+"_"+channel+spectrum).c_str(),("rrv_high"+label+"_"+channel+spectrum).c_str(),0.5,0.,1.);
      RooAddPdf* model_pdf  = new RooAddPdf(("model_pdf"+label+"_"+channel+spectrum).c_str(),("model_pdf"+label+"_"+channel+spectrum).c_str(),RooArgList(*erfExp,*gaus),RooArgList(*rrv_high));

      return model_pdf ;
    }
  // FOR MC FITS TO MATCHED TT MC!!!  
    if( model == "GausErfExp_ttbar"){

      double mean1_tmp = 8.1653e+01;
      double sigma1_tmp = 6.5932e+00;
      float rangeMean = 4. ;
      float rangeWidth = 5. ;
      double frac_tmp = 0.6;
      double c0_tmp     = -2.7180e-02 ;      //double c0_tmp_err     = 6.83e-03;
      double offset_tmp =  8.6888e+01 ;      //double offset_tmp_err = 9.35e+00;
      double width_tmp  =  3.9860e+01 ;      //double width_tmp_err  = 2.97e+00;  

      RooRealVar* rrv_mean1_gaus  = new RooRealVar(("rrv_mean1_gaus"+label+"_"+channel+spectrum).c_str(),("rrv_mean1_gaus"+label+"_"+channel+spectrum).c_str(),mean1_tmp, mean1_tmp-rangeMean, mean1_tmp+rangeMean);
      RooRealVar* rrv_sigma1_gaus = new RooRealVar(("rrv_sigma1_gaus"+label+"_"+channel+spectrum).c_str(),("rrv_sigma1_gaus"+label+"_"+channel+spectrum).c_str(),sigma1_tmp, sigma1_tmp-rangeWidth,sigma1_tmp+rangeWidth );
      RooGaussian* gaus1 = new RooGaussian(("gaus1"+label+"_"+channel+spectrum).c_str(),("gaus1"+label+"_"+channel+spectrum).c_str(),*rrv_x,*rrv_mean1_gaus,*rrv_sigma1_gaus);

      RooRealVar* rrv_frac = new RooRealVar(("rrv_frac"+label+"_"+channel+spectrum).c_str(),("rrv_frac"+label+"_"+channel+spectrum).c_str(),frac_tmp,0.4,1);
      RooRealVar* rrv_c_ErfExp      = new RooRealVar(("rrv_c_ErfExp"+label+"_"+channel+spectrum).c_str(),("rrv_c_ErfExp"+label+"_"+channel+spectrum).c_str(),c0_tmp,-10,10.);
      RooRealVar* rrv_offset_ErfExp = new RooRealVar(("rrv_offset_ErfExp"+label+"_"+channel+spectrum).c_str(),("rrv_offset_ErfExp"+label+"_"+channel+spectrum).c_str(),offset_tmp,0.,150.);
      RooRealVar* rrv_width_ErfExp  = new RooRealVar(("rrv_width_ErfExp"+label+"_"+channel+spectrum).c_str(),("rrv_width_ErfExp"+label+"_"+channel+spectrum).c_str(),width_tmp,0.,150.);


      
      RooErfExpPdf* erfExp = new RooErfExpPdf(("erfExp"+label+"_"+channel+spectrum).c_str(),("model_pdf"+label+"_"+channel+spectrum).c_str(),*rrv_x,*rrv_c_ErfExp,*rrv_offset_ErfExp,*rrv_width_ErfExp);
      RooAddPdf* model_pdf = new RooAddPdf(("model_pdf"+label+"_"+channel+spectrum).c_str(),("model_pdf"+label+"_"+channel+spectrum).c_str(),RooArgList(*gaus1,*erfExp),RooArgList(*rrv_frac),1);

      return model_pdf ;

    }

    if( model == "2Gaus_ttbar"){

      double mean1_tmp = 8.5934e+01;
      double sigma1_tmp = 8.1149e+00;
      float rangeMean = 5. ;
      float rangeWidth = 5. ;
      double frac_tmp = 7.3994e-01 ;
      double deltamean_tmp  = 9.499 ;
      double scalesigma_tmp = 2.5752;

      if(TString(wtagger_label.c_str()).Contains("76X")){
        frac_tmp = 7.3739e-01 ; 
        deltamean_tmp  = 7.81599999999998829e+00 ;
        scalesigma_tmp = 2.74416583258705149e+00;
      }

      RooRealVar* rrv_mean1_gaus  = new RooRealVar(("rrv_mean1_gaus"+label+"_"+channel+spectrum).c_str(),("rrv_mean1_gaus"+label+"_"+channel+spectrum).c_str(),mean1_tmp, mean1_tmp-rangeMean, mean1_tmp+rangeMean);
      RooRealVar* rrv_sigma1_gaus = new RooRealVar(("rrv_sigma1_gaus"+label+"_"+channel+spectrum).c_str(),("rrv_sigma1_gaus"+label+"_"+channel+spectrum).c_str(),sigma1_tmp, sigma1_tmp-rangeWidth,sigma1_tmp+rangeWidth );

      if( TString(label.c_str()).Contains("fail") ){
        if( TString(label).Contains("data") ) {
          rrv_mean1_gaus  = workspace->var(("rrv_mean1_gaus_ttbar_data_"+channel+spectrum).c_str());
          rrv_sigma1_gaus = workspace->var(("rrv_sigma1_gaus_ttbar_data_"+channel+spectrum).c_str());
        }
        else if( TString(label).Contains("TotalMC") ) {
          rrv_mean1_gaus  = workspace->var(("rrv_mean1_gaus_ttbar_TotalMC_"+channel+spectrum).c_str());
          rrv_sigma1_gaus = workspace->var(("rrv_sigma1_gaus_ttbar_TotalMC_"+channel+spectrum).c_str());
        }
      }

      RooGaussian* gaus1 = new RooGaussian(("gaus1"+label+"_"+channel+spectrum).c_str(),("gaus1"+label+"_"+channel+spectrum).c_str(),*rrv_x,*rrv_mean1_gaus,*rrv_sigma1_gaus);

      

      RooRealVar* rrv_deltamean_gaus  = new RooRealVar(("rrv_deltamean_gaus"+label+"_"+channel+spectrum).c_str(),("rrv_deltamean_gaus"+label+"_"+channel+spectrum).c_str(),deltamean_tmp,0,30);
      RooFormulaVar* rrv_mean2_gaus   = new RooFormulaVar(("rrv_mean2_gaus"+label+"_"+channel+spectrum).c_str(),"@0+@1",RooArgList(*rrv_mean1_gaus,*rrv_deltamean_gaus));
      RooRealVar* rrv_scalesigma_gaus = new RooRealVar(("rrv_scalesigma_gaus"+label+"_"+channel+spectrum).c_str(),("rrv_scalesigma_gaus"+label+"_"+channel+spectrum).c_str(),scalesigma_tmp,0,5);
      RooFormulaVar* rrv_sigma2_gaus  = new RooFormulaVar(("rrv_sigma2_gaus"+label+"_"+channel+spectrum).c_str(),"@0*@1", RooArgList(*rrv_sigma1_gaus,*rrv_scalesigma_gaus));
      RooGaussian* gaus2 = new RooGaussian(("gaus2"+label+"_"+channel+spectrum).c_str(),("gaus2"+label+"_"+channel+spectrum).c_str(), *rrv_x,*rrv_mean2_gaus,*rrv_sigma2_gaus);      std::cout<< "######## Testing 1,2 ########"<<std::endl;                                                                                                                                                                          
                                                                                                                                                                                                                                       
      RooRealVar* rrv_frac = new RooRealVar(("rrv_frac"+label+"_"+channel+spectrum).c_str(),("rrv_frac"+label+"_"+channel+spectrum).c_str(),frac_tmp,0,1);//,frac_tmp-frac_tmp_err,frac_tmp+frac_tmp_err);                            \
                                                                                                                                                                                                                                       
      std::cout<< "######## Testing 1,2,3. ########"<<std::endl;                                                                                                                                                                       
                                                                                                                                                                                                                                       
      RooAddPdf* model_pdf = new RooAddPdf(("model_pdf"+label+"_"+channel+spectrum).c_str(),("model_pdf"+label+"_"+channel+spectrum).c_str(),RooArgList(*gaus1,*gaus2),RooArgList(*rrv_frac),1);                                       
        

      //RooRealVar* rrv_frac = new RooRealVar(("rrv_frac"+label+"_"+channel+spectrum).c_str(),("rrv_frac"+label+"_"+channel+spectrum).c_str(),frac_tmp,0,1);//,frac_tmp-frac_tmp_err,frac_tmp+frac_tmp_err);
      // RooAddPdf* model_pdf = new RooAddPdf(("model_pdf"+label+"_"+channel+spectrum).c_str(),("model_pdf"+label+"_"+channel+spectrum).c_str(),RooArgList(*gaus1,*gaus2),RooArgList(*rrv_frac),1);

      return model_pdf ;
    }



    /*
    if( model == "2Gaus"){

      double mean1_tmp = 8.1934e+01;
      double sigma1_tmp = 8.1149e+00;
      float rangeMean = 50. ;
      float rangeWidth = 25. ;
      double frac_tmp = 0.2 ;
      double deltamean_tmp  = 49.499 ;
      double scalesigma_tmp = 1.5752;
 
      std::cout<< "######## 2 Gaussian fit to bkg  ########"<<std::endl;
      // ??? cout 
      RooRealVar* rrv_mean1_gaus  = new RooRealVar(("rrv_mean1_gaus"+label+"_"+channel+spectrum).c_str(),("rrv_mean1_gaus"+label+"_"+channel+spectrum).c_str(),mean1_tmp, mean1_tmp-rangeMean, mean1_tmp+rangeMean);
      RooRealVar* rrv_sigma1_gaus = new RooRealVar(("rrv_sigma1_gaus"+label+"_"+channel+spectrum).c_str(),("rrv_sigma1_gaus"+label+"_"+channel+spectrum).c_str(),sigma1_tmp, sigma1_tmp-rangeWidth,sigma1_tmp+rangeWidth );

      if( TString(label.c_str()).Contains("fail") ){
        if( TString(label).Contains("data") ) {
          rrv_mean1_gaus  = workspace->var(("rrv_mean1_gaus_ttbar_data_"+channel+spectrum).c_str());
          rrv_sigma1_gaus = workspace->var(("rrv_sigma1_gaus_ttbar_data_"+channel+spectrum).c_str());
        }
        else if( TString(label).Contains("TotalMC") ) {
          rrv_mean1_gaus  = workspace->var(("rrv_mean1_gaus_ttbar_TotalMC_"+channel+spectrum).c_str());
          rrv_sigma1_gaus = workspace->var(("rrv_sigma1_gaus_ttbar_TotalMC_"+channel+spectrum).c_str());
        }
      }

      RooGaussian* gaus1 = new RooGaussian(("gaus1"+label+"_"+channel+spectrum).c_str(),("gaus1"+label+"_"+channel+spectrum).c_str(),*rrv_x,*rrv_mean1_gaus,*rrv_sigma1_gaus);
      std::cout<< "######## Testing ########"<<std::endl;


      RooRealVar* rrv_deltamean_gaus  = new RooRealVar(("rrv_deltamean_gaus"+label+"_"+channel+spectrum).c_str(),("rrv_deltamean_gaus"+label+"_"+channel+spectrum).c_str(),deltamean_tmp,0,60);
      RooFormulaVar* rrv_mean2_gaus   = new RooFormulaVar(("rrv_mean2_gaus"+label+"_"+channel+spectrum).c_str(),"@0+@1",RooArgList(*rrv_mean1_gaus,*rrv_deltamean_gaus));
      RooRealVar* rrv_scalesigma_gaus = new RooRealVar(("rrv_scalesigma_gaus"+label+"_"+channel+spectrum).c_str(),("rrv_scalesigma_gaus"+label+"_"+channel+spectrum).c_str(),scalesigma_tmp,0,6);
      RooFormulaVar* rrv_sigma2_gaus  = new RooFormulaVar(("rrv_sigma2_gaus"+label+"_"+channel+spectrum).c_str(),"@0*@1", RooArgList(*rrv_sigma1_gaus,*rrv_scalesigma_gaus));
      RooGaussian* gaus2 = new RooGaussian(("gaus2"+label+"_"+channel+spectrum).c_str(),("gaus2"+label+"_"+channel+spectrum).c_str(), *rrv_x,*rrv_mean2_gaus,*rrv_sigma2_gaus);
      std::cout<< "######## Testing 1,2 ########"<<std::endl;

      RooRealVar* rrv_frac = new RooRealVar(("rrv_frac"+label+"_"+channel+spectrum).c_str(),("rrv_frac"+label+"_"+channel+spectrum).c_str(),frac_tmp,0,1);//,frac_tmp-frac_tmp_err,frac_tmp+frac_tmp_err);                                                                                                                                                                    
      std::cout<< "######## Testing 1,2,3. ########"<<std::endl;

      RooAddPdf* model_pdf = new RooAddPdf(("model_pdf"+label+"_"+channel+spectrum).c_str(),("model_pdf"+label+"_"+channel+spectrum).c_str(),RooArgList(*gaus1,*gaus2),RooArgList(*rrv_frac),1);

      return model_pdf ;
    }


    */

  // FOR MC FITS TO MATCHED TT MC!!! 
    if( model == "GausChebychev_ttbar_failSubjetTau21cut"){

      RooAbsPdf* model_pdf = NULL ;

      double p0_tmp = 3.1099e-01 ; double p0_tmp_err = 1.86e-01;
      double p1_tmp = -2.2128e-01; double p1_tmp_err = 3.02e-01;
      double frac_tmp =  4.6400e-01  ; double frac_tmp_err = 1.20e-01;

      if(TString(wtagger_label.c_str()).Contains("76X")){
        p0_tmp = 2.1208e-01 ;
        p1_tmp = -3.2198e-01;
        frac_tmp = 4.3714e-01;
      }

      // take the same gaussian used in the pass sample
      RooAbsPdf* gaus = NULL ;
      if( TString(label).Contains("data"   ) ) gaus = workspace->pdf(("gaus1_ttbar_data_"+channel+spectrum).c_str());
      if( TString(label).Contains("TotalMC") ) gaus = workspace->pdf(("gaus1_ttbar_TotalMC_"+channel+spectrum).c_str());
      if( TString(label).Contains("realW")   ) gaus = workspace->pdf(("gaus1_TTbar_realW_"+channel+spectrum).c_str());
      double mean1_tmp = 8.9682e+01;
      double sigma1_tmp = 12.;


      //RooRealVar* rrv_mean1_gaus = new RooRealVar(("rrv_mean1_gaus"+label+"_"+channel+spectrum).c_str(),("rrv_mean1_gaus"+label+"_"+channel+spectrum).c_str(),mean1_tmp, 75., 95.);
      //RooRealVar* rrv_sigma1_gaus = new RooRealVar(("rrv_sigma1_gaus"+label+"_"+channel+spectrum).c_str(),("rrv_sigma1_gaus"+label+"_"+channel+spectrum).c_str(),sigma1_tmp,3.,19. );
      //RooGaussian* gaus = new RooGaussian(("gaus"+label+"_"+channel+spectrum).c_str(),("gaus1"+label+"_"+channel+spectrum).c_str(),*rrv_x,*rrv_mean1_gaus,*rrv_sigma1_gaus);

      RooRealVar* rrv_p0_cheb = new RooRealVar(("rrv_p0_cheb"+label+"_"+channel+spectrum).c_str(),("rrv_p0_cheb"+label+"_"+channel+spectrum).c_str(),p0_tmp,0.,1.);
      RooRealVar* rrv_p1_cheb = new RooRealVar(("rrv_p1_cheb"+label+"_"+channel+spectrum).c_str(),("rrv_p1_cheb"+label+"_"+channel+spectrum).c_str(),p1_tmp,-1.,0.);//,p1_tmp-p1_tmp_err,p1_tmp+p1_tmp_err);

      RooChebychev* cheb = new RooChebychev(("cheb"+label+"_"+channel+spectrum).c_str(),("cheb"+label+"_"+channel+spectrum).c_str(), *rrv_x, RooArgList(*rrv_p0_cheb,*rrv_p1_cheb) );

      RooRealVar* rrv_frac = new RooRealVar(("rrv_frac"+label+"_"+channel+spectrum).c_str(),("rrv_frac"+label+"_"+channel+spectrum).c_str(),frac_tmp,0.,1.);
      model_pdf = new RooAddPdf(("model_pdf"+label+"_"+channel+spectrum).c_str(),("model_pdf"+label+"_"+channel+spectrum).c_str(),RooArgList(*gaus,*cheb),RooArgList(*rrv_frac),1);

      return model_pdf ;
    }

    if( model == "GausErfExp_ttbar_failSubjetTau21cut"){

      double c0_tmp     = -5.5276e-02;      double c0_tmp_err = 1.46e-02;
      double offset_tmp = 198. ;      double offset_tmp_err = 4.92e+01;
      double width_tmp  = 64.8  ;      double width_tmp_err = 4.69e+00;
      double frac_tmp   = 0.4;
      
      RooAbsPdf* model_pdf = NULL ;
      
      // take the same gaussian used in the pass sample
      RooAbsPdf* gaus = NULL ;
      if( TString(label).Contains("data"   ) ) gaus = workspace->pdf(("gaus1_ttbar_data_"+channel+spectrum).c_str());
      if( TString(label).Contains("TotalMC") ) gaus = workspace->pdf(("gaus1_ttbar_TotalMC_"+channel+spectrum).c_str());
      if( TString(label).Contains("realW")   ) gaus = workspace->pdf(("gaus1_TTbar_realW_"+channel+spectrum).c_str());
      
      //double mean1_tmp  = 8.7486e+01; if( model == "ErfExp_ttbar"){
      //double sigma1_tmp = 8.7456e+00;
      //     RooRealVar* rrv_mean1_gaus  = new RooRealVar(("rrv_mean1_gaus"+label+"_"+channel+spectrum).c_str(),("rrv_mean1_gaus"+label+"_"+channel+spectrum).c_str(),mean1_tmp, mean1_tmp-15, mean1_tmp+15);
      //     RooRealVar* rrv_sigma1_gaus = new RooRealVar(("rrv_sigma1_gaus"+label+"_"+channel+spectrum).c_str(),("rrv_sigma1_gaus"+label+"_"+channel+spectrum).c_str(),sigma1_tmp, sigma1_tmp-3,sigma1_tmp+3 );
      //     RooGaussian* gaus = new RooGaussian(("gaus"+label+"_"+channel+spectrum).c_str(),("gaus1"+label+"_"+channel+spectrum).c_str(),*rrv_x,*rrv_mean1_gaus,*rrv_sigma1_gaus);
      //
      
      //RooRealVar* rrv_mean1_gaus = new RooRealVar(("rrv_mean1_gaus"+label+"_"+channel+spectrum).c_str(),("rrv_mean1_gaus"+label+"_"+channel+spectrum).c_str(),mean1_tmp, 75., 90.);
      //RooRealVar* rrv_sigma1_gaus = new RooRealVar(("rrv_sigma1_gaus"+label+"_"+channel+spectrum).c_str(),("rrv_sigma1_gaus"+label+"_"+channel+spectrum).c_str(),sigma1_tmp,5.,15. );
      //RooGaussian* gaus = new RooGaussian(("gaus"+label+"_"+channel+spectrum).c_str(),("gaus1"+label+"_"+channel+spectrum).c_str(),*rrv_x,*rrv_mean1_gaus,*rrv_sigma1_gaus);


      RooRealVar* rrv_c_ErfExp = new RooRealVar(("rrv_c_ErfExp"+label+"_"+channel+spectrum).c_str(),("rrv_c_ErfExp"+label+"_"+channel+spectrum).c_str(),c0_tmp,-0.1,0.);//,c0_tmp-4e-2, c0_tmp+4e-2);
      RooRealVar* rrv_offset_ErfExp = new RooRealVar(("rrv_offset_ErfExp"+label+"_"+channel+spectrum).c_str(),("rrv_offset_ErfExp"+label+"_"+channel+spectrum).c_str(),offset_tmp,0.,200.);//,offset_tmp-offset_tmp_err,offset_tmp+offset_tmp_err);
      RooRealVar* rrv_width_ErfExp = new RooRealVar(("rrv_width_ErfExp"+label+"_"+channel+spectrum).c_str(),("rrv_width_ErfExp"+label+"_"+channel+spectrum).c_str(), width_tmp,0.,100);//,width_tmp-width_tmp_err, width_tmp+width_tmp_err);

      RooErfExpPdf* erfExp = new RooErfExpPdf(("erfExp"+label+"_"+channel+spectrum).c_str(),("model_pdf"+label+"_"+channel+spectrum).c_str(),*rrv_x,*rrv_c_ErfExp,*rrv_offset_ErfExp,*rrv_width_ErfExp);

      RooRealVar* rrv_frac = new RooRealVar(("rrv_frac"+label+"_"+channel+spectrum).c_str(),("rrv_frac"+label+"_"+channel+spectrum).c_str(),frac_tmp,0.,1.);
      
      model_pdf = new RooAddPdf(("model_pdf"+label+"_"+channel+spectrum).c_str(),("model_pdf"+label+"_"+channel+spectrum).c_str(),RooArgList(*gaus,*erfExp),RooArgList(*rrv_frac),1);

      return model_pdf ;
    }

    if( model == "ErfExp_ttbar"){

      double c0_tmp     = -2.7180e-02 ;      double c0_tmp_err     = 6.83e-03;
      double offset_tmp =  8.6888e+01 ;      double offset_tmp_err = 9.35e+00;
      double width_tmp  =  2.9860e+01 ;      double width_tmp_err  = 2.97e+00;

      if(TString(wtagger_label.c_str()).Contains("76X")){
        c0_tmp     = -1.9681e-02 ;
        offset_tmp =  7.4564e+01 ;
        width_tmp  =  2.6397e+01 ;
      }
      if(TString(wtagger_label.c_str()).Contains("0v60")){
        c0_tmp     = -2.9373e-02 ;  
        offset_tmp =  8.2980e+01 ;
        width_tmp  =  3.6133e+01 ;
        if(TString(wtagger_label.c_str()).Contains("76X")){
          c0_tmp     = -2.2689e-02 ;
          offset_tmp =  6.9803e+01 ;
          width_tmp  =  3.2077e+01 ;
        }
      }
      if(TString(wtagger_label.c_str()).Contains("DDT")){
        c0_tmp     = -6.0079e-02 ;
        offset_tmp =  1.4980e+02 ;
        width_tmp  =  4.8168e+01 ;
        if(TString(wtagger_label.c_str()).Contains("0v52")){
          c0_tmp = -3.1793e-02    ;     
          offset_tmp = 9.7997e+01 ;    
          width_tmp = 3.8820e+01  ;
        }
        
      }
      
      RooRealVar* rrv_c_ErfExp      = new RooRealVar(("rrv_c_ErfExp"+label+"_"+channel+spectrum).c_str(),("rrv_c_ErfExp"+label+"_"+channel+spectrum).c_str(),c0_tmp,c0_tmp-4e-2, c0_tmp+4e-2 );
      RooRealVar* rrv_offset_ErfExp = new RooRealVar(("rrv_offset_ErfExp"+label+"_"+channel+spectrum).c_str(),("rrv_offset_ErfExp"+label+"_"+channel+spectrum).c_str(),offset_tmp,offset_tmp-offset_tmp_err*4,offset_tmp+offset_tmp_err*4);
      RooRealVar* rrv_width_ErfExp  = new RooRealVar(("rrv_width_ErfExp"+label+"_"+channel+spectrum).c_str(),("rrv_width_ErfExp"+label+"_"+channel+spectrum).c_str(),width_tmp, width_tmp-10, width_tmp+10);

      RooErfExpPdf* model_pdf = new RooErfExpPdf(("model_pdf"+label+"_"+channel+spectrum).c_str(),("model_pdf"+label+"_"+channel+spectrum).c_str(),*rrv_x,*rrv_c_ErfExp,*rrv_offset_ErfExp,*rrv_width_ErfExp);

      RooGaussian* gaus1 = addConstraint(rrv_c_ErfExp,rrv_c_ErfExp->getVal(),c0_tmp_err,constraint);
      RooGaussian* gaus2 = addConstraint(rrv_offset_ErfExp,rrv_offset_ErfExp->getVal(),offset_tmp_err,constraint);
      RooGaussian* gaus3 = addConstraint(rrv_width_ErfExp,rrv_width_ErfExp->getVal(),width_tmp_err,constraint);
      workspace->import(*gaus1);
      workspace->import(*gaus2);
      workspace->import(*gaus3);
      return model_pdf ;
    }
    // Matched tt fit
    if( model == "ErfExp_ttbar_failSubjetTau21cut"){

      RooErfExpPdf* model_pdf = NULL ;

      double c0_tmp = -3.0626e-02    ;      double c0_tmp_err = 1.46e-02;
      double offset_tmp = 5.1636e+01 ;      double offset_tmp_err = 4.92e+01;
      double width_tmp = 3.6186e+01  ;      double width_tmp_err = 4.69e+00;

      if(TString(wtagger_label.c_str()).Contains("76X")){
        c0_tmp = -2.8654e-02    ;
        offset_tmp = 4.5140e+01 ;
        width_tmp = 3.4083e+01  ;
      }
      if(TString(wtagger_label.c_str()).Contains("0v60")){
        c0_tmp = -3.4131e-02    ;  
        offset_tmp = 3.3961e+01 ;
        width_tmp = 3.2876e+01  ;
        if(TString(wtagger_label.c_str()).Contains("76X")){
          c0_tmp = -3.3221e-02    ; 
          offset_tmp = 2.9445e+01 ;
          width_tmp = 2.5680e+01  ;
        }
      }
      if(TString(wtagger_label.c_str()).Contains("DDT")){
        c0_tmp     = -5.9405e-02 ;
        offset_tmp =  1.4790e+02 ;
        width_tmp  =  5.3544e+01 ;
        if(TString(wtagger_label.c_str()).Contains("0v52")){
          c0_tmp = -4.0722e-02    ;     
          offset_tmp = 1.0108e+02 ;    
          width_tmp = 4.9796e+01  ;
        }
      }

      RooRealVar* rrv_c_ErfExp = new RooRealVar(("rrv_c_ErfExp"+label+"_"+channel+spectrum).c_str(),("rrv_c_ErfExp"+label+"_"+channel+spectrum).c_str(),c0_tmp,c0_tmp-4e-2, c0_tmp+4e-2);
      RooRealVar* rrv_offset_ErfExp = new RooRealVar(("rrv_offset_ErfExp"+label+"_"+channel+spectrum).c_str(),("rrv_offset_ErfExp"+label+"_"+channel+spectrum).c_str(),offset_tmp,0.,200.);
      RooRealVar* rrv_width_ErfExp = new RooRealVar(("rrv_width_ErfExp"+label+"_"+channel+spectrum).c_str(),("rrv_width_ErfExp"+label+"_"+channel+spectrum).c_str(), width_tmp,0,100.);

      model_pdf = new RooErfExpPdf(("model_pdf"+label+"_"+channel+spectrum).c_str(),("model_pdf"+label+"_"+channel+spectrum).c_str(),*rrv_x,*rrv_c_ErfExp,*rrv_offset_ErfExp,*rrv_width_ErfExp);
      RooGaussian* gaus1 = addConstraint(rrv_c_ErfExp,rrv_c_ErfExp->getVal(),c0_tmp_err,constraint);
      workspace->import(*gaus1);
      return model_pdf ;
    }
  }  
  else if( TString(label).Contains("fakeW")){ // Background component of ttbar fit
    if( model == "GausErfExp_ttbar_fakeW"){

      double mean1_tmp =  8.553e+01;         // 8.153e+01;
      double sigma1_tmp = 8.5932e+00;
      float rangeMean =   5. ;
      float rangeWidth =  5. ;
      double frac_tmp =   0.6;
      double c0_tmp     = -2.7180e-02 ;      //double c0_tmp_err     = 6.83e-03;
      double offset_tmp =  8.6888e+01 ;      //double offset_tmp_err = 9.35e+00;
      double width_tmp  =  2.9860e+01 ;      //double width_tmp_err  = 2.97e+00;  

      RooRealVar* rrv_mean1_gaus  = new RooRealVar(("rrv_mean1_gaus"+label+"_"+channel+spectrum).c_str(),("rrv_mean1_gaus"+label+"_"+channel+spectrum).c_str(),mean1_tmp, mean1_tmp-rangeMean, mean1_tmp+rangeMean);
      RooRealVar* rrv_sigma1_gaus = new RooRealVar(("rrv_sigma1_gaus"+label+"_"+channel+spectrum).c_str(),("rrv_sigma1_gaus"+label+"_"+channel+spectrum).c_str(),sigma1_tmp, sigma1_tmp-rangeWidth,sigma1_tmp+rangeWidth );
      RooGaussian* gaus1 = new RooGaussian(("gaus1"+label+"_"+channel+spectrum).c_str(),("gaus1"+label+"_"+channel+spectrum).c_str(),*rrv_x,*rrv_mean1_gaus,*rrv_sigma1_gaus);

      RooRealVar* rrv_frac = new RooRealVar(("rrv_frac"+label+"_"+channel+spectrum).c_str(),("rrv_frac"+label+"_"+channel+spectrum).c_str(),frac_tmp,0.4,1);
      RooRealVar* rrv_c_ErfExp      = new RooRealVar(("rrv_c_ErfExp"+label+"_"+channel+spectrum).c_str(),("rrv_c_ErfExp"+label+"_"+channel+spectrum).c_str(),c0_tmp,-10,10.);
      RooRealVar* rrv_offset_ErfExp = new RooRealVar(("rrv_offset_ErfExp"+label+"_"+channel+spectrum).c_str(),("rrv_offset_ErfExp"+label+"_"+channel+spectrum).c_str(),offset_tmp,0.,150.);
      RooRealVar* rrv_width_ErfExp  = new RooRealVar(("rrv_width_ErfExp"+label+"_"+channel+spectrum).c_str(),("rrv_width_ErfExp"+label+"_"+channel+spectrum).c_str(),width_tmp,0.,150.);


      
      RooErfExpPdf* erfExp = new RooErfExpPdf(("erfExp"+label+"_"+channel+spectrum).c_str(),("model_pdf"+label+"_"+channel+spectrum).c_str(),*rrv_x,*rrv_c_ErfExp,*rrv_offset_ErfExp,*rrv_width_ErfExp);
      RooAddPdf* model_pdf = new RooAddPdf(("model_pdf"+label+"_"+channel+spectrum).c_str(),("model_pdf"+label+"_"+channel+spectrum).c_str(),RooArgList(*gaus1,*erfExp),RooArgList(*rrv_frac),1);

      return model_pdf ;
    }
    
    if( model == "GausErfExp_ttbar_failSubjetTau21cut"){

      double c0_tmp     = -5.5276e-02;      double c0_tmp_err = 1.46e-02;
      double offset_tmp = 198. ;      double offset_tmp_err = 4.92e+01;
      double width_tmp  = 64.8  ;      double width_tmp_err = 4.69e+00;
      double frac_tmp   = 0.4;
      
      RooAbsPdf* model_pdf = NULL ;
      
      // take the same gaussian used in the pass sample
      RooAbsPdf* gaus = NULL ;
      if( TString(label).Contains("data"   ) ) gaus = workspace->pdf(("gaus1_ttbar_data_"+channel+spectrum).c_str());
      if( TString(label).Contains("TotalMC") ) gaus = workspace->pdf(("gaus1_ttbar_TotalMC_"+channel+spectrum).c_str());
      if( TString(label).Contains("realW")   ) gaus = workspace->pdf(("gaus1_TTbar_realW_"+channel+spectrum).c_str());
      
      //double mean1_tmp  = 8.7486e+01; if( model == "ErfExp_ttbar"){
      //double sigma1_tmp = 8.7456e+00;
      //     RooRealVar* rrv_mean1_gaus  = new RooRealVar(("rrv_mean1_gaus"+label+"_"+channel+spectrum).c_str(),("rrv_mean1_gaus"+label+"_"+channel+spectrum).c_str(),mean1_tmp, mean1_tmp-15, mean1_tmp+15);
      //     RooRealVar* rrv_sigma1_gaus = new RooRealVar(("rrv_sigma1_gaus"+label+"_"+channel+spectrum).c_str(),("rrv_sigma1_gaus"+label+"_"+channel+spectrum).c_str(),sigma1_tmp, sigma1_tmp-3,sigma1_tmp+3 );
      //     RooGaussian* gaus = new RooGaussian(("gaus"+label+"_"+channel+spectrum).c_str(),("gaus1"+label+"_"+channel+spectrum).c_str(),*rrv_x,*rrv_mean1_gaus,*rrv_sigma1_gaus);
      //
      
      //RooRealVar* rrv_mean1_gaus = new RooRealVar(("rrv_mean1_gaus"+label+"_"+channel+spectrum).c_str(),("rrv_mean1_gaus"+label+"_"+channel+spectrum).c_str(),mean1_tmp, 75., 90.);
      //RooRealVar* rrv_sigma1_gaus = new RooRealVar(("rrv_sigma1_gaus"+label+"_"+channel+spectrum).c_str(),("rrv_sigma1_gaus"+label+"_"+channel+spectrum).c_str(),sigma1_tmp,5.,15. );
      //RooGaussian* gaus = new RooGaussian(("gaus"+label+"_"+channel+spectrum).c_str(),("gaus1"+label+"_"+channel+spectrum).c_str(),*rrv_x,*rrv_mean1_gaus,*rrv_sigma1_gaus);


      RooRealVar* rrv_c_ErfExp = new RooRealVar(("rrv_c_ErfExp"+label+"_"+channel+spectrum).c_str(),("rrv_c_ErfExp"+label+"_"+channel+spectrum).c_str(),c0_tmp,-0.1,0.);//,c0_tmp-4e-2, c0_tmp+4e-2);
      RooRealVar* rrv_offset_ErfExp = new RooRealVar(("rrv_offset_ErfExp"+label+"_"+channel+spectrum).c_str(),("rrv_offset_ErfExp"+label+"_"+channel+spectrum).c_str(),offset_tmp,0.,200.);//,offset_tmp-offset_tmp_err,offset_tmp+offset_tmp_err);
      RooRealVar* rrv_width_ErfExp = new RooRealVar(("rrv_width_ErfExp"+label+"_"+channel+spectrum).c_str(),("rrv_width_ErfExp"+label+"_"+channel+spectrum).c_str(), width_tmp,0.,100);//,width_tmp-width_tmp_err, width_tmp+width_tmp_err);

      RooErfExpPdf* erfExp = new RooErfExpPdf(("erfExp"+label+"_"+channel+spectrum).c_str(),("model_pdf"+label+"_"+channel+spectrum).c_str(),*rrv_x,*rrv_c_ErfExp,*rrv_offset_ErfExp,*rrv_width_ErfExp);

      RooRealVar* rrv_frac = new RooRealVar(("rrv_frac"+label+"_"+channel+spectrum).c_str(),("rrv_frac"+label+"_"+channel+spectrum).c_str(),frac_tmp,0.,1.);
      
      model_pdf = new RooAddPdf(("model_pdf"+label+"_"+channel+spectrum).c_str(),("model_pdf"+label+"_"+channel+spectrum).c_str(),RooArgList(*gaus,*erfExp),RooArgList(*rrv_frac),1);

      return model_pdf ;
    }

    if( model == "GausChebychev_ttbar_failSubjetTau21cut"){

      RooAbsPdf* model_pdf = NULL ;

      double p0_tmp = 3.1099e-01 ; double p0_tmp_err = 1.86e-01;
      double p1_tmp = -2.2128e-01; double p1_tmp_err = 3.02e-01;
      double frac_tmp =  4.6400e-01  ; double frac_tmp_err = 1.20e-01;

      if(TString(wtagger_label.c_str()).Contains("76X")){
        p0_tmp = 2.1208e-01 ;
        p1_tmp = -3.2198e-01;
        frac_tmp = 4.3714e-01;
      }

      // take the same gaussian used in the pass sample
      RooAbsPdf* gaus = NULL ;
      if( TString(label).Contains("data"   ) ) gaus = workspace->pdf(("gaus1_ttbar_data_"+channel+spectrum).c_str());
      if( TString(label).Contains("TotalMC") ) gaus = workspace->pdf(("gaus1_ttbar_TotalMC_"+channel+spectrum).c_str());
      if( TString(label).Contains("realW")   ) gaus = workspace->pdf(("gaus1_TTbar_realW_"+channel+spectrum).c_str());
      //double mean1_tmp = 8.9682e+01;
      //double sigma1_tmp = 12.;


      ///RooRealVar* rrv_mean1_gaus = new RooRealVar(("rrv_mean1_gaus"+label+"_"+channel+spectrum).c_str(),("rrv_mean1_gaus"+label+"_"+channel+spectrum).c_str(),mean1_tmp, 75., 105.);
      //RooRealVar* rrv_sigma1_gaus = new RooRealVar(("rrv_sigma1_gaus"+label+"_"+channel+spectrum).c_str(),("rrv_sigma1_gaus"+label+"_"+channel+spectrum).c_str(),sigma1_tmp,11.,22. );
      //RooGaussian* gaus = new RooGaussian(("gaus"+label+"_"+channel+spectrum).c_str(),("gaus1"+label+"_"+channel+spectrum).c_str(),*rrv_x,*rrv_mean1_gaus,*rrv_sigma1_gaus);

      RooRealVar* rrv_p0_cheb = new RooRealVar(("rrv_p0_cheb"+label+"_"+channel+spectrum).c_str(),("rrv_p0_cheb"+label+"_"+channel+spectrum).c_str(),p0_tmp,0.,1.);
      RooRealVar* rrv_p1_cheb = new RooRealVar(("rrv_p1_cheb"+label+"_"+channel+spectrum).c_str(),("rrv_p1_cheb"+label+"_"+channel+spectrum).c_str(),p1_tmp,-1.,0.);//,p1_tmp-p1_tmp_err,p1_tmp+p1_tmp_err);

      RooChebychev* cheb = new RooChebychev(("cheb"+label+"_"+channel+spectrum).c_str(),("cheb"+label+"_"+channel+spectrum).c_str(), *rrv_x, RooArgList(*rrv_p0_cheb,*rrv_p1_cheb) );

      RooRealVar* rrv_frac = new RooRealVar(("rrv_frac"+label+"_"+channel+spectrum).c_str(),("rrv_frac"+label+"_"+channel+spectrum).c_str(),frac_tmp,0.,1.);
      model_pdf = new RooAddPdf(("model_pdf"+label+"_"+channel+spectrum).c_str(),("model_pdf"+label+"_"+channel+spectrum).c_str(),RooArgList(*gaus,*cheb),RooArgList(*rrv_frac),1);

      return model_pdf ;
    }
  }
  return NULL;
} //End



