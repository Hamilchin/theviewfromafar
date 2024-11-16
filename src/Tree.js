// PostList.js
import React, { Component } from 'react';

class Tree extends Component {
    render() {
      return (
        <div className="tree">
          <pre>
            {`                                                        .
                                                .         ;
                   .              .              ;%     ;;   
                     ,           ,                :;%  %;   
                      :         ;               [`}
            <a href="#philosophy" onClick={() => this.props.onSelectCategory('philosophy')}>philosophy</a>
            {`]  .,   
             ,.        %;     %;            ;        %;'    ,;
               ;       ;%;  %%;        ,     %;    ;%;    ,%'
                %;       %;%;      ,  ;       %;  ;%;   ,%;' 
                 ;%;   [`}
            <a href="#poetry" onClick={() => this.props.onSelectCategory('poetry')}>poetry</a>
            {`]     ;%;        % ;%;  ,%;'
                  \`%;.     ;%;     %;'         \`%;%;.%;'
                   \`:%;.    ;%%. %@;        %; ;@%;%'
                      \`:%;.  :;&#%;          %;@%;'
                        \`@%:.  :;%.         ;@@%;'   
                          \`@%.  \`;@%.      ;@@%;         
                            \`@%%. \`@%%    ;@@%;        
                              ;@%. :@%%  %@@%;       
                                %@&)%%%&(%%:;     
                                  #@%%%%%:;;
                                  %#@@%%::;
                                  %#@@o%:;;  . '         
                                  %#@@o%;:(.,'         
                              \`.. %@@(o)::;         
                                 \`)#@@o%::;         
                                  %#@@o%::;        
                                 .%#@@@%::;         
                                 ;%#@@@%::;.          
                                ;%#@@@%%:;;;. 
                            ...;%#@[`}
            <a href="#about" onClick={() => this.props.onSelectCategory('about')}>about</a>
            {`];;;...                            `}
          </pre>
        </div>
      );
    }
  }
  
export default Tree;
